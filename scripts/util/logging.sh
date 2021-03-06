### ARGUMENTS
## $1: The message you want to print
## $2: The name of the script from which the message originated

### DESCRIPTION
## Prints the inputted message with the current time and with
## text formatting. 
log(){
    echo -e "\e[92m$(date +"%r")\e[0m: \e[4;32m$2\e[0m : >> $1"
}

# DESCRIPTION
## Prints the script name and the script description
## with new lines in between for formatting.
help(){
    nl=$'\n'
    echo -e "${nl}\e[4m$2\e[0m${nl}${nl}   $1" 
}

concat_args(){
    if [ ! $# -eq 0 ]
    then
        ARG_STRING=""
        for arg in $@
        do
            ARG_STRING="$ARG_STRING $1"
            shift
        done
        echo $ARG_STRING
    fi
}