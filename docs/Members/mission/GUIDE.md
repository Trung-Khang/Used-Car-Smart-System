# GIT_GUIDE.md — Hướng dẫn sử dụng Git cho nhóm

## 1. Mục đích

Tài liệu này quy định workflow Git chung cho project:

```text
used-car-smart-system/
```

Mục tiêu:

- Mỗi thành viên làm việc trên branch riêng.
- Không commit trực tiếp vào `main`.
- Hạn chế conflict.
- Luôn đồng bộ code trước khi bắt đầu công việc.
- Khi có thay đổi chưa commit, phải bảo vệ thay đổi trước khi pull/rebase.
- Pull Request là cách chính để đưa code vào `main` hoặc `develop` nếu nhóm sử dụng branch `develop`.

---

# 2. Quy ước Branch

Chỉ có 5 branches chính: Main, TV1, TV2, TV3, TV4, TV5

KHÔNG ĐƯỢC TẠO THÊM BẤT KÌ BRANCH NÀO KHÁC!

Tên branch nên mô tả rõ công việc.

---

# 3. Kiểm tra Git đã cài

```bash
git --version
```

Thiết lập lần đầu:

```bash
git config --global user.name "Tên Của Bạn"
git config --global user.email "email-cua-ban@example.com"
```

Kiểm tra:

```bash
git config --global --list
```

---

# 4. Clone project về máy

Lấy URL repository trên GitHub.

Ví dụ:

```bash
git clone https://github.com/Trung-Khang/Used-Car-Smart-System
```

Đi vào project:

```bash
cd used-car-smart-system
```

Kiểm tra:

```bash
git status
git remote -v
```

Kết quả mong muốn có remote:

```text
origin
```

---

# 5. Xem branch hiện có

```bash
git branch
```

Xem cả branch local và remote:

```bash
git branch -a
```

Ví dụ:

```text
* main
  remotes/origin/main
```

---

# 6. CHUYỂN SANG BRANCH CỦA MÌNH

```bash
git checkout TV...
```
Kiểm tra:

```bash
git branch
```

Branch hiện tại phải có dấu `*`.


# 7. Workflow chuẩn mỗi khi bắt đầu làm việc

Mỗi lần mở project để làm việc:

```bash
git switch main
git pull origin main
git switch feature/<branch-cua-ban>
```

Sau đó cập nhật branch của mình bằng main.

Cách ưu tiên:

```bash
git fetch origin
git rebase origin/main
```

Hoặc:

```bash
git pull origin main --rebase
```

Sau khi rebase xong mới bắt đầu code.

---

# 9. Trong lúc code

Kiểm tra trạng thái thường xuyên:

```bash
git status
```

Xem file thay đổi:

```bash
git diff
```

Không nên chờ code quá lâu mới commit.

Nên commit theo từng phần logic hoàn chỉnh.

Ví dụ:

```text
Implement vehicle search API
Add valuation service
Create vehicle card UI
Add crawler price cleaning
Integrate R prediction API
```

---

# 10. Add file vào staging

Xem file:

```bash
git status
```

Add tất cả:

```bash
git add .
```

Hoặc add chọn từng file:

```bash
git add backend/src/...
```

Kiểm tra staging:

```bash
git status
```

---

# 11. Commit

Commit:

```bash
git commit -m "feat(....thư mục code.....): nội dung code"
```
Ví dụ:

```bash
git commit -m "feat (crawler/src/cleaner): add cleaner"
```

---

# 12. Nếu commit không được vì còn thay đổi chưa phù hợp

Trước tiên xem:

```bash
git status
```

Nếu cần tạm cất thay đổi an toàn để tiếp tục pull/rebase:

```bash
git stash push -m "WIP before rebase"
```

Hoặc ngắn:

```bash
git stash
```

Kiểm tra:

```bash
git stash list
```

Sau khi cập nhật branch:

```bash
git stash pop
```

Nếu muốn an toàn hơn và chưa muốn xóa stash ngay:

```bash
git stash apply
```

`apply` giữ lại stash; `pop` áp dụng rồi xóa stash nếu áp dụng thành công.

---

# 13. Quy trình an toàn khi có code chưa commit mà cần pull

Không nên làm:

```bash
git pull origin main
```

khi đang có thay đổi local quan trọng mà chưa commit.


```bash
git status
git diff
```

Nếu mọi thứ ổn:

```bash
git add .
git commit -m "feat(....): ..."
git push -u oringin TV....
```

---

# 14. Khi pull bị lỗi do branch local và remote khác nhau

Ưu tiên sử dụng:

```bash
git pull origin main --rebase
```


# 15. Nếu xảy ra conflict khi rebase

Git có thể báo:

```text
CONFLICT (content): Merge conflict in ...
```

## Bước 1 — Xem file conflict

```bash
git status
```

## Bước 2 — Mở file

Bạn sẽ thấy:

```text
<<<<<<< HEAD
Code từ main
=======
Code của branch bạn
>>>>>>> ...
```

Cần tự quyết định giữ:

```text
Code main
```

hay:

```text
Code branch của bạn
```

hoặc kết hợp cả hai.

Sau khi sửa, xóa các marker:

```text
<<<<<<<
=======
>>>>>>>
```

## Bước 3 — Add file đã sửa

```bash
git add <file>
```

Ví dụ:

```bash
git add backend/src/main/java/com/usedcar/system/service/VehicleService.java
```

## Bước 4 — Tiếp tục rebase

```bash
git rebase --continue
```

Lặp lại nếu còn conflict.

---


# 16. Git workflow cuối cùng của nhóm

```text
                 GitHub
                   │
                 main
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
     TV1        TV2        TV3/4/5
   Backend    Frontend      Modules
        │          │          │
        └──────────┼──────────┘
                   ▼
              Pull Request
                   │
                 Review
                   │
                   ▼
               main/develop
```

Mục tiêu là mọi thành viên có thể làm việc song song nhưng code chỉ được hợp nhất sau khi kiểm tra và xử lý conflict đúng cách.

---
