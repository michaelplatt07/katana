" Vim Syntax File
" Language: Katana
" Maintainer: Michael Platt
" Latest Revision: 2023-12-30

hi KatanaMain ctermfg=94
hi KatanaVarDecKeyword ctermfg=29
hi KatanaBuiltinMethods ctermfg=130
hi KatanaLogic ctermfg=140
hi KatanaComment ctermfg=202
hi KatanaConst ctermfg=180
hi KatanaString ctermfg=191
hi KatanaVar ctermfg=191
hi KatanaChar ctermfg=191

" Main keyword
syn keyword katanaKeyword main 
highlight link katanaKeyword KatanaMain

" Variable declaration keywords
syn keyword katanaVarKeyword int8 int16 int32 int64 bool char const string MACRO nil
highlight link katanaVarKeyword KatanaVarDecKeyword

" Builtin function keywords
syn keyword katanaBuiltinFuncKeyword charAt print printl copyStr
highlight link katanaBuiltinFuncKeyword KatanaBuiltinMethods

" Function declarations
syntax region katanaFunction start="fn \zs" end="\ze::"
highlight link katanaFunction KatanaFunction
match katanaBuiltinFuncKeyword /fn/
highlight link katanaBuiltinFuncKeyword KatanaBuiltinMethods

" Builtin constant var values
syn keyword katanaBuiltinVarsKeyword true false idx
highlight link katanaBuiltinVarsKeyword KatanaConst

" Logic keywords
syn keyword katanaLogicKeyword if else loopUp loopDown loopFrom iLoopUp iLoopDown iLoopFrom
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
