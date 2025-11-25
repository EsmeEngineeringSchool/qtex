# La coloration syntaxique avec vim

## `syntax/qtex.vim`
```vim
syntax match qtexKey      "#\w\+" skipwhite nextgroup=qtexEntry, contained
syntax match qtexKey "#END \w\+" skipwhite nextgroup=qtexKey contained
syntax region LaTeXRegion start=/\\(/ end=/\\)/ contained
syntax match qtexLaTeX1 "\$\$[^$]\+\$\$"
syntax match qtexLaTeX2 "\\(\_.\{-}\\)" containedin=LaTeXRegion
syntax include @Python syntax/python.vim
syntax region PythonRegion matchgroup=qtexKey start=/#CR_PRELOAD/ end=/#END CR_PRELOAD/ contains=@Python
syntax region PythonRegion matchgroup=qtexKey start=/#CR_ANSWER/ end=/#END CR_ANSWER/ contains=@Python
syntax region PythonRegion matchgroup=qtexKey start=/#CR_CASE_CODE/ end=/#END CR_CASE_CODE/ contains=@Python
syntax region PythonRegion matchgroup=qtexKey start=/#CR_TEMPLATE/ end=/#END CR_TEMPLATE/ contains=@Python    
```

## `ftdetect/qtex.vim`
```vim
autocmd BufRead,BufNewFile *.qtex set filetype=qtex
```
