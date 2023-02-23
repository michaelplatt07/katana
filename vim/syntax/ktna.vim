" Vim Syntax File
" Language: Katana
" Maintainer: Michael Platt
" Latest Revision: 2023-02-23

hi KatanaMain ctermfg=94
hi KatanaVarDecKeyword ctermfg=29
hi KatanaBuiltinMethods ctermfg=130
hi KatanaLogic ctermfg=140
hi KatanaComment ctermfg=202
hi KatanaString ctermfg=191
hi KatanaChar ctermfg=191

" Main keyword
syn keyword katanaKeyword main 
highlight link katanaKeyword KatanaMain

" Variable declaration keywords
syn keyword katanaVarKeyword int16 bool char const string 
highlight link katanaVarKeyword KatanaVarDecKeyword

" Builtin function keywords
syn keyword katanaBuiltinFuncKeyword charAt print printl
highlight link katanaBuiltinFuncKeyword KatanaBuiltinMethods

" Logic keywords
syn keyword katanaLogicKeyword if else loopUp loopDown loopFrom
highlight link katanaLogicKeyword KatanaLogic

" Comments
syntax match katanaComment "\v//.*$"
highlight link katanaComment KatanaComment

" String
syntax region katanaString start=/\v"/ skip=/\v\\./ end=/\v"/
highlight link katanaString KatanaString

" Char
syntax region katanaChar start=/\v'/ skip=/\v\\./ end=/\v'/
highlight link katanaChar KatanaChar
