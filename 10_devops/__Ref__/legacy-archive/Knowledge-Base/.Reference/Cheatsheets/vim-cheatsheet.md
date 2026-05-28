# Vim Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Vim editor commands for quick reference -- Các lệnh Vim editor để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Modes](#modes) -- Các chế độ
- [Navigation](#navigation) -- Điều hướng
- [Editing](#editing) -- Chỉnh sửa
- [Search & Replace](#search--replace) -- Tìm kiếm và Thay thế
- [Visual Mode](#visual-mode) -- Chế độ Visual
- [Copy & Paste](#copy--paste) -- Sao chép và Dán
- [Files & Buffers](#files--buffers) -- Files và Buffers
- [Windows & Tabs](#windows--tabs) -- Cửa sổ và Tabs
- [Macros](#macros) -- Macros
- [Configuration](#configuration) -- Cấu hình

## <a id="modes"></a> Modes -- Các chế độ

```
# Vim modes -- Các chế độ Vim
Normal mode      Default mode for navigation and commands -- Chế độ mặc định cho điều hướng và lệnh
Insert mode      Text editing mode -- Chế độ chỉnh sửa văn bản
Visual mode      Text selection mode -- Chế độ chọn văn bản
Command mode     Execute commands -- Thực thi lệnh

# Switch modes -- Chuyển chế độ
i                Enter Insert mode at cursor -- Vào Insert tại con trỏ
I                Enter Insert mode at line start -- Vào Insert tại đầu dòng
a                Enter Insert mode after cursor -- Vào Insert sau con trỏ
A                Enter Insert mode at line end -- Vào Insert tại cuối dòng
o                New line below, enter Insert -- Dòng mới dưới, vào Insert
O                New line above, enter Insert -- Dòng mới trên, vào Insert
v                Enter Visual mode -- Vào Visual mode
V                Enter Visual Line mode -- Vào Visual Line mode
Ctrl+v           Enter Visual Block mode -- Vào Visual Block mode
:                Enter Command mode -- Vào Command mode
Esc              Return to Normal mode -- Trở về Normal mode
```

## <a id="navigation"></a> Navigation -- Điều hướng

```
# Basic movement -- Di chuyển cơ bản
h                Move left -- Di chuyển trái
j                Move down -- Di chuyển xuống
k                Move up -- Di chuyển lên
l                Move right -- Di chuyển phải

# Word movement -- Di chuyển theo từ
w                Next word start -- Đầu từ tiếp theo
W                Next WORD start (space-separated) -- Đầu WORD tiếp theo
e                Next word end -- Cuối từ tiếp theo
E                Next WORD end -- Cuối WORD tiếp theo
b                Previous word start -- Đầu từ trước
B                Previous WORD start -- Đầu WORD trước

# Line movement -- Di chuyển theo dòng
0                Line start -- Đầu dòng
^                First non-blank character -- Ký tự không trắng đầu tiên
$                Line end -- Cuối dòng
g_               Last non-blank character -- Ký tự không trắng cuối

# Screen movement -- Di chuyển màn hình
H                Screen top -- Đỉnh màn hình
M                Screen middle -- Giữa màn hình
L                Screen bottom -- Đáy màn hình
Ctrl+u           Half page up -- Nửa trang lên
Ctrl+d           Half page down -- Nửa trang xuống
Ctrl+b           Full page up -- Trang lên
Ctrl+f           Full page down -- Trang xuống

# Document movement -- Di chuyển trong tài liệu
gg               Document start -- Đầu tài liệu
G                Document end -- Cuối tài liệu
:n               Go to line n -- Đến dòng n
50G              Go to line 50 -- Đến dòng 50
%                Jump to matching bracket -- Nhảy đến ngoặc khớp

# Jump movement -- Di chuyển nhảy
Ctrl+o           Jump back -- Nhảy lùi
Ctrl+i           Jump forward -- Nhảy tới
``               Jump to last position -- Nhảy đến vị trí cuối

# Marks -- Đánh dấu
ma               Set mark 'a' -- Đặt đánh dấu 'a'
`a               Jump to mark 'a' -- Nhảy đến đánh dấu 'a'
'a               Jump to mark 'a' line start -- Nhảy đến đầu dòng đánh dấu 'a'
:marks           List all marks -- Liệt kê tất cả đánh dấu
```

## <a id="editing"></a> Editing -- Chỉnh sửa

```
# Insert text -- Chèn văn bản
i                Insert before cursor -- Chèn trước con trỏ
I                Insert at line start -- Chèn tại đầu dòng
a                Append after cursor -- Thêm sau con trỏ
A                Append at line end -- Thêm tại cuối dòng
o                Open line below -- Mở dòng dưới
O                Open line above -- Mở dòng trên

# Delete -- Xóa
x                Delete character -- Xóa ký tự
X                Delete character before -- Xóa ký tự trước
dd               Delete line -- Xóa dòng
D                Delete to line end -- Xóa đến cuối dòng
dw               Delete word -- Xóa từ
d$               Delete to line end -- Xóa đến cuối dòng
d0               Delete to line start -- Xóa đến đầu dòng
dG               Delete to document end -- Xóa đến cuối tài liệu
dgg              Delete to document start -- Xóa đến đầu tài liệu

# Change (delete + insert) -- Thay đổi (xóa + chèn)
cc               Change line -- Thay đổi dòng
C                Change to line end -- Thay đổi đến cuối dòng
cw               Change word -- Thay đổi từ
ci"              Change inside quotes -- Thay đổi trong ngoặc kép
ca"              Change around quotes -- Thay đổi bao quanh ngoặc kép
ci(              Change inside parentheses -- Thay đổi trong ngoặc tròn
ci{              Change inside braces -- Thay đổi trong ngoặc nhọn

# Replace -- Thay thế
r                Replace character -- Thay thế ký tự
R                Enter Replace mode -- Vào chế độ Replace

# Undo & Redo -- Hoàn tác và Làm lại
u                Undo -- Hoàn tác
Ctrl+r           Redo -- Làm lại
U                Undo line changes -- Hoàn tác thay đổi dòng

# Other editing -- Chỉnh sửa khác
.                Repeat last command -- Lặp lại lệnh cuối
J                Join lines -- Nối dòng
>>               Indent line -- Thụt lề dòng
<<               Unindent line -- Bỏ thụt lề dòng
==               Auto-indent line -- Tự động thụt lề dòng
~                Toggle case -- Chuyển đổi hoa/thường
```

## <a id="search--replace"></a> Search & Replace -- Tìm kiếm và Thay thế

```
# Search -- Tìm kiếm
/pattern         Search forward -- Tìm kiếm tiến
?pattern         Search backward -- Tìm kiếm lùi
n                Next match -- Kết quả tiếp theo
N                Previous match -- Kết quả trước
*                Search word under cursor -- Tìm từ dưới con trỏ
#                Search word under cursor (backward) -- Tìm từ dưới con trỏ (lùi)
/\c              Case insensitive -- Không phân biệt hoa thường
/\C              Case sensitive -- Phân biệt hoa thường

# Replace -- Thay thế
:s/old/new       Replace first on line -- Thay thế đầu tiên trên dòng
:s/old/new/g     Replace all on line -- Thay thế tất cả trên dòng
:%s/old/new/g    Replace all in file -- Thay thế tất cả trong file
:%s/old/new/gc   Replace with confirm -- Thay thế có xác nhận
:5,12s/old/new/g Replace in lines 5-12 -- Thay thế trong dòng 5-12
:'<,'>s/old/new/g Replace in selection -- Thay thế trong vùng chọn

# Clear search highlight -- Xóa highlight tìm kiếm
:noh             No highlight -- Không highlight
:nohlsearch      No highlight search -- Không highlight tìm kiếm
```

## <a id="visual-mode"></a> Visual Mode -- Chế độ Visual

```
# Enter visual mode -- Vào chế độ visual
v                Character selection -- Chọn ký tự
V                Line selection -- Chọn dòng
Ctrl+v           Block selection -- Chọn khối

# Expand selection -- Mở rộng vùng chọn
aw               Select word -- Chọn từ
ab               Select () block -- Chọn khối ()
aB               Select {} block -- Chọn khối {}
at               Select tag block -- Chọn khối tag
ib               Select inside () -- Chọn trong ()
iB               Select inside {} -- Chọn trong {}

# Actions in visual mode -- Hành động trong visual mode
d                Delete selection -- Xóa vùng chọn
y                Yank (copy) selection -- Sao chép vùng chọn
c                Change selection -- Thay đổi vùng chọn
>                Indent selection -- Thụt lề vùng chọn
<                Unindent selection -- Bỏ thụt lề vùng chọn
=                Auto-indent selection -- Tự động thụt lề vùng chọn
~                Toggle case -- Chuyển đổi hoa/thường
u                Lowercase -- Chữ thường
U                Uppercase -- Chữ hoa
```

## <a id="copy--paste"></a> Copy & Paste -- Sao chép và Dán

```
# Yank (copy) -- Sao chép
yy               Yank line -- Sao chép dòng
Y                Yank line -- Sao chép dòng
yw               Yank word -- Sao chép từ
y$               Yank to line end -- Sao chép đến cuối dòng
yG               Yank to document end -- Sao chép đến cuối tài liệu

# Paste -- Dán
p                Paste after cursor -- Dán sau con trỏ
P                Paste before cursor -- Dán trước con trỏ
]p               Paste with indent -- Dán với thụt lề

# Registers -- Thanh ghi
"ay              Yank to register a -- Sao chép vào thanh ghi a
"ap              Paste from register a -- Dán từ thanh ghi a
"+y              Yank to system clipboard -- Sao chép vào clipboard hệ thống
"+p              Paste from system clipboard -- Dán từ clipboard hệ thống
:reg             Show all registers -- Hiển thị tất cả thanh ghi
```

## <a id="files--buffers"></a> Files & Buffers -- Files và Buffers

```
# File operations -- Thao tác file
:w               Save file -- Lưu file
:w filename      Save as -- Lưu như
:wq              Save and quit -- Lưu và thoát
:x               Save and quit (if modified) -- Lưu và thoát (nếu sửa đổi)
ZZ               Save and quit -- Lưu và thoát
:q               Quit -- Thoát
:q!              Quit without saving -- Thoát không lưu
ZQ               Quit without saving -- Thoát không lưu
:e filename      Edit file -- Chỉnh sửa file
:e!              Reload file -- Tải lại file
:saveas filename Save as new file -- Lưu như file mới

# Buffer operations -- Thao tác buffer
:ls              List buffers -- Liệt kê buffers
:bn              Next buffer -- Buffer tiếp theo
:bp              Previous buffer -- Buffer trước
:b n             Go to buffer n -- Đến buffer n
:b filename      Go to buffer by name -- Đến buffer theo tên
:bd              Delete buffer -- Xóa buffer
:bd!             Force delete buffer -- Xóa buffer cưỡng chế
```

## <a id="windows--tabs"></a> Windows & Tabs -- Cửa sổ và Tabs

```
# Window splits -- Chia cửa sổ
:sp filename     Horizontal split -- Chia ngang
:vsp filename    Vertical split -- Chia dọc
Ctrl+w s         Horizontal split -- Chia ngang
Ctrl+w v         Vertical split -- Chia dọc

# Window navigation -- Điều hướng cửa sổ
Ctrl+w h         Go to left window -- Đến cửa sổ trái
Ctrl+w j         Go to bottom window -- Đến cửa sổ dưới
Ctrl+w k         Go to top window -- Đến cửa sổ trên
Ctrl+w l         Go to right window -- Đến cửa sổ phải
Ctrl+w w         Cycle windows -- Luân chuyển cửa sổ

# Window resize -- Thay đổi kích thước cửa sổ
Ctrl+w +         Increase height -- Tăng chiều cao
Ctrl+w -         Decrease height -- Giảm chiều cao
Ctrl+w >         Increase width -- Tăng chiều rộng
Ctrl+w <         Decrease width -- Giảm chiều rộng
Ctrl+w =         Equal size -- Kích thước bằng nhau

# Window close -- Đóng cửa sổ
Ctrl+w q         Close window -- Đóng cửa sổ
Ctrl+w o         Close other windows -- Đóng cửa sổ khác

# Tabs -- Tabs
:tabnew          New tab -- Tab mới
:tabnew filename New tab with file -- Tab mới với file
gt               Next tab -- Tab tiếp theo
gT               Previous tab -- Tab trước
:tabclose        Close tab -- Đóng tab
:tabonly         Close other tabs -- Đóng tabs khác
```

## <a id="macros"></a> Macros

```
# Record macro -- Ghi macro
qa               Start recording to register a -- Bắt đầu ghi vào thanh ghi a
q                Stop recording -- Dừng ghi

# Play macro -- Phát macro
@a               Play macro from register a -- Phát macro từ thanh ghi a
@@               Repeat last macro -- Lặp lại macro cuối
5@a              Play macro 5 times -- Phát macro 5 lần

# View macro -- Xem macro
:reg a           Show register a content -- Hiển thị nội dung thanh ghi a
```

## <a id="configuration"></a> Configuration -- Cấu hình

```vim
" Basic settings in .vimrc -- Cấu hình cơ bản trong .vimrc
set number                   " Show line numbers -- Hiển thị số dòng
set relativenumber           " Relative line numbers -- Số dòng tương đối
set tabstop=4                " Tab width -- Độ rộng tab
set shiftwidth=4             " Indent width -- Độ rộng thụt lề
set expandtab                " Use spaces instead of tabs -- Dùng spaces thay tabs
set autoindent               " Auto-indent -- Tự động thụt lề
set smartindent              " Smart indent -- Thụt lề thông minh
set hlsearch                 " Highlight search -- Highlight tìm kiếm
set incsearch                " Incremental search -- Tìm kiếm tăng dần
set ignorecase               " Case insensitive search -- Tìm kiếm không phân biệt hoa thường
set smartcase                " Smart case search -- Tìm kiếm thông minh
set wrap                     " Wrap lines -- Xuống dòng
set cursorline               " Highlight current line -- Highlight dòng hiện tại
set mouse=a                  " Enable mouse -- Bật chuột
set clipboard=unnamedplus    " Use system clipboard -- Dùng clipboard hệ thống
syntax on                    " Syntax highlighting -- Highlight cú pháp
```

```
# Commands in vim -- Lệnh trong vim
:set number                  " Enable line numbers -- Bật số dòng
:set nonumber                " Disable line numbers -- Tắt số dòng
:set number!                 " Toggle line numbers -- Chuyển đổi số dòng
:set paste                   " Enable paste mode -- Bật chế độ dán
:set nopaste                 " Disable paste mode -- Tắt chế độ dán
:syntax on                   " Enable syntax highlighting -- Bật highlight cú pháp
:colorscheme desert          " Change color scheme -- Đổi bảng màu
```

---
