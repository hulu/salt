#compdef salt salt-call salt-cp

local state line curcontext="$curcontext"
 
salt_dir="${$(python2 -c 'import salt; print(salt.__file__);')%__init__*}"
_modules(){
    typeset -a _funcs
    for file in $salt_dir/modules/*${words[CURRENT]%.*}*.py; do
        module=${${file##*/}%.py}
        if ! grep '__virtual__' $file &> /dev/null; then
            continue
        fi
        mod=$(python2 -c "import salt.modules.$module as tmp; print(getattr(tmp, '__virtualname__', '$module'));")
        for func in $(awk -F'[ (]' '/^def [^_]/ {print $2}' $file); do 
            _funcs+=($mod.$func)
        done
    done
    _describe modules _funcs
}

_minions(){
    _peons=($(salt-key 2>/dev/null | tail -n +2))
    _describe Minions _peons
}

_target_options=(
    '(-E --pcre)'{-E,--pcre}'[use pcre regular expressions]:pcre:'
    '(-L --list)'{-L,--list}'[take a comma or space delimited list of servers.]:list:'
    '(-G --grain)'{-G,--grain}'[use a grain value to identify targets]:Grains:'
    '--grain-pcre[use a grain value to identify targets.]:pcre:'
    '(-N --nodegroup)'{-N,--nodegroup}'[use one of the predefined nodegroups to identify a list of targets.]:Nodegroup:'
    '(-R --range)'{-R,--range}'[use a range expression to identify targets.]:Range:'
    '(-C --compound)'{-C,--compound}'[Use multiple targeting options.]:Compound:'
    '(-I --pillar)'{-I,--pillar}'[use a pillar value to identify targets.]:Pillar:'
    '(-S --ipcidr)'{-S,--ipcidr}'[Match based on Subnet (CIDR notation) or IPv4 address.]:Cidr:'
)

_common_opts=(
    "--version[show program's version number and exit]"
    "--versions-report[show program's dependencies version number and exit]"
    '(-h --help)'{-h,--help}'[show this help message and exit]'
    '(-c --config-dir)'{-c,--config-dir}'[Pass in an alternative configuration directory.(default: /etc/salt/)]:Config Directory:_files -/'
    '(-t --timeout)'{-t,--timeout}'[Change the timeout for the running command; default=5]:Timeout (seconds):'
)

_master_options=(
    '(-s --static)'{-s,--static}'[Return the data from minions as a group after they all return.]'
    "--async[Run the salt command but don't wait for a reply]"
    '(--state-output --state_output)'{--state-output,--state_output}'[Override the configured state_output value for minion output. Default: full]:Outputs:(full terse mixed changes)'
    '--subset[Execute the routine on a random subset of the targeted minions]:Subset:'
    '(-v --verbose)'{-v,--verbose}'[Turn on command verbosity, display jid and active job queries]'
    '--hide-timeout[Hide minions that timeout]'
    '(-b --batch --batch-size)'{-b,--batch,--batch-size}'[Execute the salt job in batch mode, pass number or percentage to batch.]:Batch Size:'
    '(-a --auth --eauth --extrenal-auth)'{-a,--auth,--eauth,--external-auth}'[Specify an external authentication system to use.]:eauth:'
    '(-T --make-token)'{-T,--make-token}'[Generate and save an authentication token for re-use.]'
    "--return[Set an alternative return method.]:Returners:_path_files -W '$salt_dir/returners' -g '[^_]*.py(\:r)'"
    '(-d --doc --documentation)'{-d,--doc,--documentation}"[Return the documentation for the specified module]:Module:_path_files -W '$salt_dir/modules' -g '[^_]*.py(\:r)'"
    '--args-separator[Set the special argument used as a delimiter between command arguments of compound commands.]:Arg separator:'
)

_minion_options=(
    "--return[Set an alternative return method.]:Returners:_path_files -W '$salt_dir/returners' -g '[^_]*.py(\:r)'"
    '(-d --doc --documentation)'{-d,--doc,--documentation}"[Return the documentation for the specified module]:Module:_path_files -W '$salt_dir/modules' -g '[^_]*.py(\:r)'"
    '(-g --grains)'{-g,--grains}'[Return the information generated by the salt grains]'
    {*-m,*--module-dirs}'[Specify an additional directory to pull modules from.]:Module Dirs:_files -/'
    '--master[Specify the master to use.]:Master:'
    '--local[Run salt-call locally, as if there was no master running.]'
    '--file-root[Set this directory as the base file root.]:File Root:_files -/'
    '--pillar-root[Set this directory as the base pillar root.]:Pillar Root:_files -/'
    '--retcode-passthrough[Exit with the salt call retcode and not the salt binary retcode]'
    '--id[Specify the minion id to use.]:Minion ID:'
    '--skip-grains[Do not load grains.]'
    '--refresh-grains-cache[Force a refresh of the grains cache]'
)

_logging_options=(
    '(-l --log-level)'{-l,--log-level}'[Console logging log level.(default: warning)]:Log Level:(all garbage trace debug info warning error critical quiet)'
    '--log-file[Log file path. Default: /var/log/salt/master.]:Log File:_files'
    '--log-file-level=[Logfile logging log level.Default: warning]:Log Level:(all garbage trace debug info warning error critical quiet)'
)

_out_opts=(
    '(--out --output)'{--out,--output}"[Print the output using the specified outputter.]:Outputters:_path_files -W '$salt_dir/output' -g '[^_]*.py(\:r)'"
    '(--out-indent --output-indent)'{--out-indent,--output-indent}'[Print the output indented by the provided value in spaces.]:Number:'
    '(--out-file --output-file)'{--out-file,--output-file}'[Write the output to the specified file]:Output File:_files'
    '(--no-color --no-colour)'{--no-color,--no-colour}'[Disable all colored output]'
    '(--force-color --force-colour)'{--force-color,--force-colour}'[Force colored output]'
)

_salt_comp(){
    case "$service" in
        salt)
            _arguments -C \
                ':minions:_minions' \
                ':modules:_modules' \
                "$_target_options[@]" \
                "$_common_opts[@]" \
                "$_master_options[@]" \
                "$_logging_options[@]" \
                "$_out_opts[@]"
            ;;
        salt-call)
            _arguments -C \
                ':modules:_modules' \
                "$_minion_options[@]" \
                "$_common_opts[@]" \
                "$_logging_options[@]" \
                "$_out_opts[@]"
            ;;
        salt-cp)
            _arguments -C \
                ':minions:_minions' \
                "$_target_options[@]" \
                "$_common_opts[@]" \
                "$_logging_options[@]" \
                ':Source File:_files' \
                ':Destination File:_files'
            ;;
    esac
}

_salt_comp "$@"
