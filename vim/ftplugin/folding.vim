" Vim Folding File
" Language: Katana
" Maintainer: Michael Platt
" Latest Revision: 2023-02-23

setlocal foldmethod=expr
setlocal foldexpr=GetKatanaFold(v:lnum)

function! GetKataFold(lnum)
    return '0'
endfunction


