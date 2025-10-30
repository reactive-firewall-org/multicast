#! /bin/bash
# Disclaimer of Warranties.
# A. YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT, TO THE EXTENT PERMITTED BY
#    APPLICABLE LAW, USE OF THIS SHELL SCRIPT AND ANY SERVICES PERFORMED
#    BY OR ACCESSED THROUGH THIS SHELL SCRIPT IS AT YOUR SOLE RISK AND
#    THAT THE ENTIRE RISK AS TO SATISFACTORY QUALITY, PERFORMANCE, ACCURACY AND
#    EFFORT IS WITH YOU.
#
# B. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SHELL SCRIPT
#    AND SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE", WITH ALL FAULTS AND
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
#
# Tool to lint Makefiles using checkmake.
# Validates Makefile syntax and enforces best practices.
#
# .github/tool_checkmake.sh
readonly SCRIPT_NAME="${0##*/}"

# local build path fix-up
if [[ -d "./checkmake" ]] && [[ ":$PATH:" != *":./checkmake:"* ]] ; then
	if [[ -x "./checkmake/checkmake" ]]; then
		# shellcheck disable=SC2123
		PATH="${PATH:+"$PATH:"}./checkmake" ;
		export PATH ;
	else
		readonly LOC_DESC="Local checkmake found but not executable."
		printf "%s\n" "::warning file=${SCRIPT_NAME},title=PATH::${LOC_DESC}" >&2
	fi
fi

# USAGE:
#  ~$ check_command CMD
# Arguments:
# CMD (Required) -- Name of the command to check
# Results:
#    exits 64 -- missing required argument
#    exits 126 -- check complete and has failed, can not find given command.
#    returns successful -- check complete and command found to be executable.
function check_command() {
	test -z "$1" && { printf "%s\n" "::warning file=${SCRIPT_NAME},title=BUG::Command name is required to check for existence." >&2 ; exit 64 ; } ;
	local cmd="$1" ;
	# shellcheck disable=SC2086
	test -x "$(command -v ${cmd})" || { printf "%s\n" "::error file=${SCRIPT_NAME},title=MISSING::Required command '${cmd}' is not found." >&2 ; exit 126 ; } ;
}  # end check_command()
# propagate/export function to sub-shells
export -f check_command

# Check required commands
check_command sed ;
check_command grep ;
check_command cut ;
check_command go ;

check_command checkmake ;

# USAGE:
#   ~$ usage
# Arguments:
#   None
# Results:
#   Prints usage information and exits with status code 2.
function usage() {
	printf "Usage: %s <makefile_path>\n" "${SCRIPT_NAME}" >&2
	exit 2
}

# Validate parameters
if [[ "$#" -lt 1 ]] || [[ "$#" -gt 1 ]]; then
	usage
fi

# Validate file path (no path traversal)
if [[ "${1}" == *".."* ]]; then
	readonly SEC_DESC="Path traversal detected in argument."
	printf "%s\n" "::error file=${SCRIPT_NAME},title=SECURITY::${SEC_DESC}" >&2
	exit 1
fi
readonly FILE="${1}"
readonly EMSG="Checkmake linter complained."

# Check if file exists
if [[ ! -f "${FILE}" ]] || [[ ! -r "${FILE}" ]]; then
	printf "%s\n" "::error file=${FILE},title=MISSING::File '${FILE}' not found." >&2
	exit 64
elif [[ ! "${FILE}" =~ Makefile|\.mk$ ]]; then
	readonly KIND_DESC="File '${FILE}' doesn't appear to be a Makefile."
	printf "%s\n" "::error file=${FILE},title=INVALID::${KIND_DESC}" >&2
	exit 65
fi

if [[ -L "${FILE}" ]]; then
	printf "%s\n" "::warning file=${FILE},title=SYMLINK::File is a symbolic link." >&2
fi

# process_checkmake_output processes the output of checkmake for a given file.
#
# Args:
#   $1: The file to check
#   $2: The error message to display
#
# Returns:
#   0 if no lint errors found
#   1 if lint errors found or checkmake failed
process_checkmake_output() {
	local file="$1"
	local emsg="$2"

	# PATCH for GHI reactive-firewall-org/multicast#488
	local random_id="${RANDOM}${RANDOM}${RANDOM}${RANDOM}${RANDOM}"
	local chmk_elog="checkmake_${random_id}_error_log.log"

	# Clean up on normal exit, but preserve on error for debugging
	trap "rm -f '${chmk_elog}' 2>/dev/null || :" EXIT ;

	if ! output=$(checkmake "${file}" 2>"${chmk_elog}"); then
		# On failure, preserve log by removing trap
		trap - EXIT
		printf "%s\n" "::error title='failure'::checkmake failed!"
		local error_log
		error_log=$(head -n 5000 "${chmk_elog}")
		printf "%s '%s'\n" "::error title='stderr'::checkmake error:" "$error_log" >&2

		printf "%s\n" "${output}" | \
			sed -e 's/   /:/g' | \
			tr -s ':' | \
			cut -d: -f 3-5 | \
			grep -F "${file}" | \
			sed -E -e 's/^[[:space:]]+//g' | \
			while IFS= read -r line; do
				printf "%s\n" "::warning file=${file},title=LINT::${line} ${emsg}" >&2
			done
		return 1
	else
		printf "%s\n" "::notice file=${file},title=LINT::OK - No lint errors." >&2
	fi ;
}

process_checkmake_output "${FILE}" "${EMSG}"
