#!/bin/zsh

# A quick script, so that I can just run `source ~/_WORK/me/my-resume/dev-start.zsh` to get started :-)

# @link https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
[[ ! $ZSH_EVAL_CONTEXT =~ :file$ ]] && echo "Script must be sourced" && exit 1

cd ${0:A:h}/ # Change to the directory of the current file

source .venv/bin/activate

alias poetry='pipx run poetry==1.8.3'
alias djm='python manage.py'

# Show the alias we just defined:
alias poetry && alias djm
