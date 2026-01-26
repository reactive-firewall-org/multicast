#! /bin/bash
# Disclaimer of Warranties.
# A. YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT, TO THE EXTENT PERMITTED BY
#    APPLICABLE LAW, USE OF THIS SHELL SCRIPT AND ANY SERVICES PERFORMED
#    BY OR ACCESSED THROUGH THIS SHELL SCRIPT IS AT YOUR SOLE RISK AND
#    THAT THE ENTIRE RISK AS TO SATISFACTORY QUALITY, PERFORMANCE, ACCURACY AND
#    EFFORT IS WITH YOU.
#
# B. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SHELL SCRIPT
#    AND SERVICES ARE PROVIDED "AS IS" AND “AS AVAILABLE”, WITH ALL FAULTS AND
#    WITHOUT WARRANTY OF ANY KIND, AND THE AUTHOR OF THIS SHELL SCRIPT'S LICENSORS
#    (COLLECTIVELY REFERRED TO AS "THE AUTHOR" FOR THE PURPOSES OF THIS DISCLAIMER)
#    HEREBY DISCLAIM ALL WARRANTIES AND CONDITIONS WITH RESPECT TO THIS SHELL SCRIPT
#    SOFTWARE AND SERVICES, EITHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
#    NOT LIMITED TO, THE IMPLIED WARRANTIES AND/OR CONDITIONS OF
#    MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE,
#    ACCURACY, QUIET ENJOYMENT, AND NON-INFRINGEMENT OF THIRD PARTY RIGHTS.
#
# C. THE AUTHOR DOES NOT WARRANT AGAINST INTERFERENCE WITH YOUR ENJOYMENT OF THE
#    THE AUTHOR's SOFTWARE AND SERVICES, THAT THE FUNCTIONS CONTAINED IN, OR
#    SERVICES PERFORMED OR PROVIDED BY, THIS SHELL SCRIPT WILL MEET YOUR
#    REQUIREMENTS, THAT THE OPERATION OF THIS SHELL SCRIPT OR SERVICES WILL
#    BE UNINTERRUPTED OR ERROR-FREE, THAT ANY SERVICES WILL CONTINUE TO BE MADE
#    AVAILABLE, THAT THIS SHELL SCRIPT OR SERVICES WILL BE COMPATIBLE OR
#    WORK WITH ANY THIRD PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES,
#    OR THAT DEFECTS IN THIS SHELL SCRIPT OR SERVICES WILL BE CORRECTED.
#    INSTALLATION OF THIS THE AUTHOR SOFTWARE MAY AFFECT THE USABILITY OF THIRD
#    PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES.
#
# D. YOU FURTHER ACKNOWLEDGE THAT THIS SHELL SCRIPT AND SERVICES ARE NOT
#    INTENDED OR SUITABLE FOR USE IN SITUATIONS OR ENVIRONMENTS WHERE THE FAILURE
#    OR TIME DELAYS OF, OR ERRORS OR INACCURACIES IN, THE CONTENT, DATA OR
#    INFORMATION PROVIDED BY THIS SHELL SCRIPT OR SERVICES COULD LEAD TO
#    DEATH, PERSONAL INJURY, OR SEVERE PHYSICAL OR ENVIRONMENTAL DAMAGE,
#    INCLUDING WITHOUT LIMITATION THE OPERATION OF NUCLEAR FACILITIES, AIRCRAFT
#    NAVIGATION OR COMMUNICATION SYSTEMS, AIR TRAFFIC CONTROL, LIFE SUPPORT OR
#    WEAPONS SYSTEMS.
#
# E. NO ORAL OR WRITTEN INFORMATION OR ADVICE GIVEN BY THE AUTHOR
#    SHALL CREATE A WARRANTY. SHOULD THIS SHELL SCRIPT OR SERVICES PROVE DEFECTIVE,
#    YOU ASSUME THE ENTIRE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
#    Limitation of Liability.
# F. TO THE EXTENT NOT PROHIBITED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHOR
#    BE LIABLE FOR PERSONAL INJURY, OR ANY INCIDENTAL, SPECIAL, INDIRECT OR
#    CONSEQUENTIAL DAMAGES WHATSOEVER, INCLUDING, WITHOUT LIMITATION, DAMAGES
#    FOR LOSS OF PROFITS, CORRUPTION OR LOSS OF DATA, FAILURE TO TRANSMIT OR
#    RECEIVE ANY DATA OR INFORMATION, BUSINESS INTERRUPTION OR ANY OTHER
#    COMMERCIAL DAMAGES OR LOSSES, ARISING OUT OF OR RELATED TO YOUR USE OR
#    INABILITY TO USE THIS SHELL SCRIPT OR SERVICES OR ANY THIRD PARTY
#    SOFTWARE OR APPLICATIONS IN CONJUNCTION WITH THIS SHELL SCRIPT OR
#    SERVICES, HOWEVER CAUSED, REGARDLESS OF THE THEORY OF LIABILITY (CONTRACT,
#    TORT OR OTHERWISE) AND EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION
#    OR LIMITATION OF LIABILITY FOR PERSONAL INJURY, OR OF INCIDENTAL OR
#    CONSEQUENTIAL DAMAGES, SO THIS LIMITATION MAY NOT APPLY TO YOU. In no event
#    shall THE AUTHOR's total liability to you for all damages (other than as may
#    be required by applicable law in cases involving personal injury) exceed
#    the amount of five dollars ($5.00). The foregoing limitations will apply
#    even if the above stated remedy fails of its essential purpose.
################################################################################

ulimit -t 1200
PATH="/bin:/sbin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:${PATH}"
# shellcheck disable=SC2086
LANG=${LANG:-"en_US"}
LC_ALL="${LC_ALL:-en_US.utf-8}"
LC_CTYPE="${LC_CTYPE:-${LC_ALL:-en_US.utf-8}}"
LC_COLLATE="${LC_COLLATE:-${LC_ALL:-en_US.utf-8}}"
umask 137

# rest of the script vars
# shellcheck disable=SC2086
ERR_FILE="${ERR_FILE:-/dev/null}"
# shellcheck disable=SC2086
# LOCK_FILE="${TMPDIR:-/tmp}/org.pak.multicast.chglog-generation-shell"
# shellcheck disable=SC2086
EXIT_CODE=0

# Function to write/over-write a one-line file

# USAGE:
#	~$ create_line FILE INPUT
# Arguments:
#	FILE (Required) -- file path to write to (will overwrite if already exists)
#	INPUT (Required) -- line/contents to write as string (newline will be appended automatically)
# Results:
#	writes a line to the file at the given path with the given input
function create_line() {
    local FILE="$1"
    local INPUT="$2"
    printf "%s\n" "${INPUT}" > "$FILE" || return 77;  # exit code 77 -- Permission Denied
}

# Function to write a line to a file

# USAGE:
#	~$ write_line FILE INPUT
# Arguments:
#	FILE (Required) -- file path to write to
#	INPUT (Required) -- line/contents to write as string (newline will be appended automatically)
# Results:
#	writes a line to the file at the given path with the given input
function write_line() {
    local FILE="$1"
    local INPUT="$2"
    printf "%s\n" "${INPUT}" >> "$FILE" || return 77;  # exit code 77 -- Permission Denied
}

# Function to mark the file metadata

# USAGE:
#	~$ mark_file FILE CMD
# Arguments:
#	FILE (Required) -- file path to modify
#	CMD (Optional) -- the xattr command to use
# Results:
#	updated file metadata
function mark_file() {
    local FILE="$1"
    local CMD="${2:-$(command -v xattr)}"
    local created_by=(-w com.apple.xcode.CreatedByBuildSystem true)

    if [ -n "$CMD" ]; then
        # shellcheck disable=SC2086
        "${CMD}" ${created_by[@]} "$FILE" 2> "${ERR_FILE}" > "${ERR_FILE}" || touch -a "$FILE"
    else
        touch -a "$FILE"
    fi
}

# Function to generate the MANIFEST.in file

# USAGE:
#	~$ generate_manifest FILE
# Arguments:
#	FILE (Required) -- file path to generate (expected to be MANIFEST.in)
# Results:
#	generates the manifest.in
function generate_manifest() {
    local FILE="${1}"
    create_line "$FILE" "include requirements.txt" || return $?
    mark_file "$FILE" || return $?
    for ITEM in "README.md" "LICENSE.md" "CHANGES.md" "HISTORY.md"; do
        write_line "$FILE" "include $ITEM" || return $?
    done
    for ITEM in ".gitignore" ".git_skipList" ".gitattributes" ".gitmodules" \
                ".deepsource.toml" ".*.ini" ".*.yml" ".*.yaml" \
                ".*.conf" "package.json" "tests/*.py"; do
        write_line "$FILE" "exclude $ITEM" || return $?
    done
    for ITEM in ".git" "codecov_env" ".DS_Store" ".local_pip_cleanup.txt"; do
        write_line "$FILE" "global-exclude $ITEM" || return $?
    done
    for ITEM in "test-reports" ".github" ".circleci" "venv" "docs"; do
        write_line "$FILE" "prune $ITEM" || return $?
    done
    return 0  # return 0 on success
}
# Main execution
function main() {
    local manifest_file="MANIFEST.in"
    local RET_CODE=1  # default of 'fail unless successful'
    generate_manifest "$manifest_file"
    RET_CODE=$?
    return $RET_CODE
}

# invoke entry point and collect result
main "$@"
EXIT_CODE=$?

# cleanup
unset ERR_FILE 2>/dev/null || : ;

# finally exit with result
exit ${EXIT_CODE:-255} ;
