"""
" Copyright 2013 Tomasz Wyderka <wyderkat@cofoh.com>
"  www.cofoh.com
" Licensed under GPL-2
""

python << PY_END
import vim
import sys
import os
# get the directory this script is in: the pyflakes python module should be installed there.
scriptdir = os.path.join( os.path.dirname(
  vim.eval('expand("<sfile>")')), 'code_upstairs.dir')
sys.path.insert(0, scriptdir)
import code_upstairs 
PY_END

if !exists('CUkeyNextLayer')
    let g:CUkeyNextLayer = '<space>.'
endif
if !exists('CUkeyPrevLayer')
    let g:CUkeyPrevLayer = '<space>,'
endif
if !exists('CUkeyNextFunction')
    let g:CUkeyNextFunction = '<space>m'
endif
if !exists('CUkeyPrevFunction')
    let g:CUkeyPrevFunction = '<space>n'
endif
if !exists('CUkeyJumpToFunction')
    let g:CUkeyJumpToFunction = '<space>b'
endif
if !exists('CUkeyJumpBack')
    let g:CUkeyJumpBack = '<space>v'
endif
if !exists('CUkeyHighlightFunction')
    let g:CUkeyHighlightFunction = '<space>/'
endif


function! CUinitbridge(args)
  python vim.command( "return %d" % code_upstairs.init( vim.eval("a:args") )  )
endfunction

" TODO double initialization error
command! -nargs=? -complete=dir CUinit call CUinit(<f-args>)
function! CUinit(...)  
  let l:init_result = CUinitbridge(a:000)
  if l:init_result == 1
    echom "Code Upstairs initialization error: missing sources (project) files "
  elseif l:init_result == 2
    echom "Code Upstairs initialization error: cannot lunch `cscope` "
  elseif l:init_result == 3
    echom "Code Upstairs initialization error: cannot lunch `pycscope` "
  else
    augroup code_upstairs
      autocmd!
      autocmd VimResized * python code_upstairs.refresh_statusline()
      autocmd CursorMoved * python code_upstairs.cursor_move_handler()
    augroup END
    exec "map <silent>" g:CUkeyNextLayer ":python code_upstairs.select_next_layer()<cr>"
    exec "map <silent>" g:CUkeyPrevLayer ":python code_upstairs.select_next_layer(inc=-1)<cr>"
    exec "map <silent>" g:CUkeyNextFunction ":python code_upstairs.select_next_fname()<cr>"
    exec "map <silent>" g:CUkeyPrevFunction ":python code_upstairs.select_next_fname(inc=-1)<cr>"
    exec "map <silent>" g:CUkeyJumpToFunction ":python code_upstairs.jump_to_fname()<cr>"
    exec "map <silent>" g:CUkeyJumpBack "<C-O>"
    exec "map <silent>" g:CUkeyHighlightFunction ":python code_upstairs.heighlight_fname()<cr>"
  endif
endfunction

command! CUshutdown call CUshutdown()
function! CUshutdown()  
  python code_upstairs.shutdown()
  autocmd! code_upstairs
  exec "unmap <silent>" g:CUkeyNextLayer
  exec "unmap <silent>" g:CUkeyPrevLayer
  exec "unmap <silent>" g:CUkeyNextFunction
  exec "unmap <silent>" g:CUkeyPrevFunction
  exec "unmap <silent>" g:CUkeyJumpToFunction
  exec "unmap <silent>" g:CUkeyJumpBack
  exec "unmap <silent>" g:CUkeyHighlightFunction
endfunction




