#!/usr/bin/env bash

set -e

update_git_source() {
    local PROGRAM=$1
    local SOURCE=$2
    local BRANCH=$3

    mkdir -p sources

    if [[ -d sources/${PROGRAM} ]]; then
        echo "Updating source of ${PROGRAM}..."
        pushd sources/${PROGRAM}/
        git checkout ${BRANCH}
        git fetch origin
        git reset --hard origin/${BRANCH}
        git checkout HEAD
        popd
    else
        echo "Downloading source of ${PROGRAM}..."
        cd sources/
        git clone ${SOURCE} ${PROGRAM}
        cd ${PROGRAM}/
        git checkout ${BRANCH}
        cd ../../
    fi
}

bootstrap_git_source() {
    local PROGRAM=$1

    echo "Bootstrapping source of ${PROGRAM}..."
    pushd sources/${PROGRAM}/
    ./bootstrap
    popd
}

get_git_commithash() {
    local PROGRAM=$1
    local BRANCH=$2

    pushd sources/${PROGRAM}/ &> /dev/null
    echo "$(git rev-parse ${BRANCH})"
    popd &> /dev/null
}

get_git_snapdate() {
    local PROGRAM=$1
    local BRANCH=$2

    pushd sources/${PROGRAM}/ &> /dev/null
    echo "$(git log -1 --date=format:"%Y%m%d" --format="%cd" ${BRANCH})"
    popd &> /dev/null
}

export_git_tarball() {
    local PROGRAM=$1
    local COMMIT=$2

    echo "Exporting source of ${PROGRAM}..."
    pushd sources/${PROGRAM}/
    tar -cJf ../../rpmbuild/SOURCES/${PROGRAM}-${COMMIT:0:7}.tar.xz --transform "s,^./,${PROGRAM}-${COMMIT}/," --exclude '.git*' .
    popd
}

get_github_commithash() {
    local PROGRAM=$1
    local PROJECT=$2
    local BRANCH=$3

    echo "$(curl -s https://api.github.com/repos/${PROJECT}/${PROGRAM}/commits/${BRANCH} | jq -r .sha)"
}

get_github_snapdate() {
    local PROGRAM=$1
    local PROJECT=$2
    local BRANCH=$3

    local GITHUB_DATE=$(curl -s https://api.github.com/repos/${PROJECT}/${PROGRAM}/commits/${BRANCH} | jq -r ".commit.committer.date")
    echo "$(date -d${GITHUB_DATE} +%Y%m%d)"
}

get_github_source() {
    local PROGRAM=$1
    local PROJECT=$2
    local COMMIT=$3

    echo "Downloading source of ${PROGRAM}..."
    wget -nc -P rpmbuild/SOURCES/ https://github.com/${PROJECT}/${PROGRAM}/archive/${COMMIT}/${PROGRAM}-${COMMIT:0:7}.tar.gz
}

export_spec() {
    local PROGRAM=$1
    local SNAPDATE=$2
    local COMMIT0=$3
    local COMMIT1=$4

    echo "Exporting SPEC for ${PROGRAM}..."
    sed -e "s/@SNAPDATE@/${SNAPDATE}/g" -e "s/@COMMIT0@/${COMMIT0}/g" -e "s/@COMMIT1@/${COMMIT1}/g" templates/${PROGRAM}.spec > rpmbuild/SPECS/${PROGRAM}.spec
}

build_srpm() {
    local PROGRAM=$1

    echo "Building SRPM for ${PROGRAM}..."
    rpmbuild --define "_topdir rpmbuild" --undefine "_disable_source_fetch" -bs "rpmbuild/SPECS/${PROGRAM}.spec"
}

push_srpm_to_copr() {
    local PROGRAM=$1

    echo "Pushing SRPM of ${PROGRAM} to Copr..."
    local SRPM=$(find rpmbuild/SRPMS -name "${PROGRAM}-*.src.rpm")
    copr-cli build aimylios/fpga-tools-nightly "${SRPM}"
}

push_spec_to_copr() {
    local PROGRAM=$1

    echo "Pushing SPEC of ${PROGRAM} to Copr..."
    copr-cli build aimylios/fpga-tools-nightly "rpmbuild/SPECS/${PROGRAM}.spec"
}

clean_rpmbuild() {
    local PROGRAM=$1

    echo "Cleaning RPM build environment for ${PROGRAM}..."
    rm -f rpmbuild/SOURCES/${PROGRAM}-*.tar.*
    rm -f rpmbuild/SPECS/${PROGRAM}.spec
    rm -f rpmbuild/SRPMS/${PROGRAM}*.src.rpm
}

# openocd
update_git_source "openocd" "https://git.code.sf.net/p/openocd/code" "master"
COMMIT=$(get_git_commithash "openocd" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "openocd"
    bootstrap_git_source "openocd"
    SNAPDATE=$(get_git_snapdate "openocd" "master")
    export_git_tarball "openocd" "${COMMIT}"
    export_spec "openocd" "${SNAPDATE}" "${COMMIT}"
    build_srpm "openocd"
    push_srpm_to_copr "openocd"
fi

# gtkwave
COMMIT=$(get_github_commithash "gtkwave" "gtkwave" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "gtkwave"
    SNAPDATE=$(get_github_snapdate "gtkwave" "gtkwave" "master")
    export_spec "gtkwave" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "gtkwave"
fi

# iverilog
COMMIT=$(get_github_commithash "iverilog" "steveicarus" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "iverilog"
    SNAPDATE=$(get_github_snapdate "iverilog" "steveicarus" "master")
    export_spec "iverilog" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "iverilog"
fi

# yosys
COMMIT=$(get_github_commithash "yosys" "YosysHQ" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "yosys"
    SNAPDATE=$(get_github_snapdate "yosys" "YosysHQ" "master")
    get_github_source "yosys" "YosysHQ" "${COMMIT}"
    export_spec "yosys" "${SNAPDATE}" "${COMMIT}"
    build_srpm "yosys"
    push_srpm_to_copr "yosys"
fi

# ghdl
COMMIT=$(get_github_commithash "ghdl" "ghdl" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "ghdl"
    SNAPDATE=$(get_github_snapdate "ghdl" "ghdl" "master")
    export_spec "ghdl" "${SNAPDATE}" "${COMMIT}"
    build_srpm "ghdl"
    push_srpm_to_copr "ghdl"
fi

# ghdl-yosys-plugin
COMMIT=$(get_github_commithash "ghdl-yosys-plugin" "ghdl" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "ghdl-yosys-plugin"
    SNAPDATE=$(get_github_snapdate "ghdl-yosys-plugin" "ghdl" "master")
    export_spec "ghdl-yosys-plugin" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "ghdl-yosys-plugin"
fi

# icestorm
COMMIT=$(get_github_commithash "icestorm" "cliffordwolf" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "icestorm"
    SNAPDATE=$(get_github_snapdate "icestorm" "cliffordwolf" "master")
    export_spec "icestorm" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "icestorm"
fi

# trellis
COMMIT0=$(get_github_commithash "prjtrellis" "SymbiFlow" "master")
if ! grep -r "${COMMIT0}" rpmbuild/SPECS/; then
    clean_rpmbuild "trellis"
    SNAPDATE=$(get_github_snapdate "prjtrellis" "SymbiFlow" "master")
    COMMIT1=$(get_github_commithash "prjtrellis-db" "SymbiFlow" "master")
    export_spec "trellis" "${SNAPDATE}" "${COMMIT0}" "${COMMIT1}"
    push_spec_to_copr "trellis"
fi

# arachne-pnr
COMMIT=$(get_github_commithash "arachne-pnr" "YosysHQ" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "arachne-pnr"
    SNAPDATE=$(get_github_snapdate "arachne-pnr" "YosysHQ" "master")
    export_spec "arachne-pnr" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "arachne-pnr"
fi

# nextpnr
COMMIT=$(get_github_commithash "nextpnr" "YosysHQ" "master")
if ! grep -r "${COMMIT}" rpmbuild/SPECS/; then
    clean_rpmbuild "nextpnr"
    SNAPDATE=$(get_github_snapdate "nextpnr" "YosysHQ" "master")
    export_spec "nextpnr" "${SNAPDATE}" "${COMMIT}"
    push_spec_to_copr "nextpnr"
fi
