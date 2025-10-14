# BÁO CÁO ĐỒ ÁN CÁ NHÂN
# Ứng dụng các thuật toán tìm kiếm trong trí tuệ nhân tạo vào bài toán 8-Rooks

## Thông tin
- **Tên báo cáo:** Ứng dụng các thuật toán tìm kiếm trong trí tuệ nhân tạo vào bài toán 8-Rooks
- **GVHD:** TS.Phan Thị Huyền Trang
- **Môn Học:** Trí tuệ nhân tạo
- **Mã học phần:** 251ARIN330585_05CLC
- Học kỳ 2 - năm học 2024 - 2025
- **Sinh viên thực hiện:** Nguyễn Khánh
- **MSSV:** 23110112

## MỤC LỤC
``nhớ điền``
## VẤN ĐỀ
1. Bối cảnh:
Bài toán 8 quân xe là một biến thể đơn giản hơn của bài toán kinh điển “8 quân hậu” trong lĩnh vực Trí tuệ nhân tạo (AI) và Bài toán thỏa mãn ràng buộc (CSP – Constraint Satisfaction Problem).
Trên bàn cờ vua kích thước 8×8, ta cần đặt 8 quân xe sao cho không có hai quân xe nào tấn công lẫn nhau.

2. Mục tiêu:
- Ứng dụng các thuật toán tìm kiếm trong AI
- So sánh hiệu suất các thuật toán
- Xây dựng giao diện minh họa
- Tìm ra tất cả các cách (hoặc ít nhất một cách) sắp xếp 8 quân xe trên bàn cờ sao cho không có hai quân xe nào nằm cùng hàng hoặc cùng cột.

## CƠ SỞ LÝ THUYẾT
### BÀI TOÁN 8 QUÂN XE
Bài toán 8 quân xe là một ma trận 2D kích thước 8x8. Mục tiêu đặt các quân xe sao cho không có quân xe nào tấn công lẫn nhau.

**Trạng thái đích**
```
#example
. R . . . . . .
. . . R . . . .
. . . . . . R .
. . . . . R . .
R . . . . . . .
. . R . . . . .
. . . . R . . .
. . . . . . . R
```
- Vì khả năng máy tính cá nhân có hạn nên không gian trạng thái được hình thành dựa trên số quân được đặt trên mỗi hàng (Không tấn công lẫn nhau)
- Mỗi trạng thái ứng với việc đặt **k quân xe** đầu tiên, mỗi hàng một quân, không trùng cột.  
→ Số trạng thái có đúng `k` quân là hoán vị chập `k` của 8:
- `phép tính`:
\[
{}_{8}P_{k} = \frac{8!}{(8-k)!}
\]
- `Bảng chi tiết`
---
| k | Công thức          | Giá trị  |
|---|--------------------|----------:|
| 0 | 8! / 8!            | 1         |
| 1 | 8! / 7!            | 8         |
| 2 | 8! / 6!            | 56        |
| 3 | 8! / 5!            | 336       |
| 4 | 8! / 4!            | 1,680     |
| 5 | 8! / 3!            | 6,720     |
| 6 | 8! / 2!            | 20,160    |
| 7 | 8! / 1!            | 40,320    |
| 8 | 8! / 0!            | 40,320    |
- 40,320 trạng thái **hoàn chỉnh** (đặt đủ 8 quân).  
- 69,281 trạng thái **chưa đủ** (đặt từ 0 → 7 quân).  

### CÁC THUẬT TOÁN TÌM KIẾM
Các thuật toán tìm kiếm được phân loại thành các nhóm chính:
1. **Thuật toán tìm kiếm không có thông tin (Uninformed Search)**: Không sử dụng thông tin bổ sung về trạng thái để hướng dẫn quá trình tìm kiếm, chỉ dựa trên cấu trúc đồ thị trạng thái và mục tiêu.
2. **Thuật toán tìm kiếm có thông tin (Informed Search)**: Sử dụng hàm heuristic(h) để ước lượng chi phí đến mục tiêu, giúp tìm kiếm hiệu quả hơn, trên mục tiêu tìm kiếm theo hướng hứa hẹn nhất.
3. **Thuật toán tìm kiếm cục bộ (Local Search)**: Các thuật toán chỉ quan tâm đến trạng thái hiện tại (tùy bài toán) thay vì duyệt toàn bộ cây tìm kiếm
4. **Thuật toán thỏa mãn ràng buộc (CSP)**: Tìm giá trị cho các biến sao cho tất cả ràng buộc đều được thỏa mãn.
5. **Thuật toán cho môi trường phức tạp**: Từ môi trường phức tạp/không chắc chắn tìm kiếm lời giải cho bài toán

### Cấu trúc đồ án
`nhớ điền`
### Công nghệ được sử dụng trong đồ án
- **Ngôn ngữ lập trình:** Python 3.12.5
- **Thư viện giao diện đồ họa:** tkinter
- **Thư viện hỗ trợ:**
  - `copy` – hỗ trợ sao chép đối tượng (deep copy)  
  - `random` – tạo số ngẫu nhiên, chọn phần tử ngẫu nhiên, tráo trộn  
  - `time` – đo thời gian chạy  
  - `collections.deque` – cấu trúc hàng đợi hai đầu (double-ended queue), dùng cho BFS hoặc hàng đợi hiệu quả  
  - `heapq` – cài đặt hàng đợi ưu tiên (priority queue) bằng heap  
  - `itertools` – cung cấp công cụ tạo tổ hợp, hoán vị, lặp vô hạn  
  - `math` – hỗ trợ các hàm toán học

## THUẬT TOÁN
### Thuật toán tìm kiếm không có thông tin
#### 1. Tìm kiếm theo chiều rộng (BFS): 
- **Nguyên lý:** Duyệt theo tầng — mở rộng tất cả trạng thái ở độ sâu hiện tại trước khi sang tầng sau, dùng hàng đợi (queue).
- **Ưu điểm:** Tìm được lời giải tối ưu (nếu có). Đảm bảo tìm thấy lời giải nếu tồn tại.
- **Nhược điểm**: Tốn bộ nhớ

#### 2. Thuật toán tìm kiếm theo chiều sâu (DFS)
- **Nguyên lý:** Duyệt theo nhánh mở rộng một trạng thái đến độ sâu có thể trước khi quay lui. Sử dụng ngăn xếp (stack) để lưu trữ trạng thái.
- **Ưu điểm:**: Ít tốn bộ nhớ hơn so với BFS.    
- **Nhược điểm:** Có thể rơi vào vòng lặp hoặc đi sâu vào nhánh sai. Không đảm bảo tìm được lời giải tối ưu.

#### 3. Tìm Kiếm Chi Phí Đồng Nhất (UCS)
- **Nguyên lý:** Thuật toán luôn mở rộng trạng thái có chi phí đường đi nhỏ nhất từ trạng thái ban đầu. Sử dụng hàng đợi ưu tiên (priority queue) để chọn nút có tổng chi phí thấp nhất.
- **Ưu điểm:**  Đảm bảo tìm được đường đi tối ưu nếu tất cả chi phí là dương. Hoạt động tốt cho các bài toán có trọng số khác nhau giữa các bước di chuyển.  
- **Nhược điểm:**  Tốc độ chậm nếu không có giới hạn chi phí hoặc đồ thị quá lớn. Cần sử dụng nhiều bộ nhớ để lưu hàng đợi ưu tiên.

#### 4. Tìm Kiếm Giới Hạn Độ Sâu (DLS)
- **Nguyên lý:** Là biến thể của DFS, nhưng đặt một giới hạn độ sâu (limit) để tránh việc thuật toán đi quá sâu vào nhánh vô hạn. Khi đạt tới giới hạn này, thuật toán quay lui (backtrack) mà không mở rộng thêm.
- **Ưu điểm:** Tránh rơi vào vòng lặp vô hạn như DFS thông thường. Tiết kiệm bộ nhớ.  
- **Nhược điểm:** Có thể bỏ sót lời giải nếu giới hạn độ sâu nhỏ hơn độ sâu thực tế của lời giải.  

#### 5. Tìm Kiếm Sâu Lặp (Iterative Deepening Search – IDS)
- **Nguyên lý:** Là sự kết hợp giữa DFS và BFS. Sử dụng DLS (Depth-Limited Search) làm hàm con. Thuật toán thực hiện tìm kiếm giới hạn độ sâu (DLS) nhiều lần, mỗi lần tăng giới hạn độ sâu thêm 1, cho đến khi tìm được lời giải. 
- **Ưu điểm:** Sẽ tìm thấy lời giải nếu tồn tại. Đảm bảo lời giải tối ưu khi chi phí giữa các bước là bằng nhau. Tiết kiệm bộ nhớ hơn BFS. Tránh vòng lặp vô hạn như DFS.  
- **Nhược điểm:** Phải duyệt lại nhiều lần các nút ở độ sâu nhỏ hơn.

### Thuật toán tìm kiếm có thông tin
#### 1. Tìm Kiếm Tham Lam (Greedy Best-First Search)
- **Nguyên lý:** Thuật toán sử dụng hàm heuristic h(n) để ước lượng khoảng cách từ trạng thái hiện tại đến đích và luôn chọn mở rộng trạng thái có giá trị heuristic nhỏ nhất (priority queue).
- **Công thức đánh giá:**  
> f(n) = h(n)
- **Ưu điểm:** Tốc độ nhanh, mở rộng ít trạng thái hơn trong nhiều trường hợp. Hiệu quả cao khi hàm heuristic được thiết kế tốt.  
- **Nhược điểm:** Không đảm bảo tìm được lời giải tối ưu, vì bỏ qua chi phí thực tế.  

#### 2. Tìm kiếm A* (A* Search)
- **Nguyên lý:** Tổng chi phí thực tế từ điểm bắt đầu đến nút hiện tại g(n) và ước lượng chi phí từ nút hiện tại đến đích(h(n).  
- Thuật toán mở rộng các nút có giá trị nhỏ nhất trong hàng đợi ưu tiên (priority queue).  
> f(n) = g(n) + h(n)  
- **Ưu điểm:**: Kết hợp được tốc độ của tìm kiếm tham lam và độ chính xác của tìm kiếm chi phí đồng nhất. Đảm bảo tìm được lời giải tối ưu nếu heuristic chấp nhận được (admissible).  
- **Nhược điểm:** Tốn nhiều bộ nhớ, do phải lưu toàn bộ các nút đã mở rộng.  Phụ thuộc vào chất lượng của hàm heuristic.

### Thuật toán tìm kiếm cục bộ
#### 1. Thuật Toán Leo Đồi (Hill Climbing)
- **Nguyên lý:** Bắt đầu từ một trạng thái ban đầu và liên tục di chuyển sang trạng thái lân cận tốt hơn dựa trên giá trị của hàm đánh giá (heuristic).  
- **Ưu điểm:** Hiệu quả với không gian trạng thái lớn (không cần duyệt toàn bộ).  
- **Nhược điểm:** Có thể mắc kẹt tại cực đại cục bộ (local maximum). Không đảm bảo tìm được nghiệm tối ưu toàn cục.

#### 2. Tìm Kiếm Tôi Luyện Mô Phỏng (Simulated Annealing)
**Nguyên lý:** Thuật toán mô phỏng quá trình tôi luyện kim loại, bắt đầu với nhiệt độ cao
(cho phép chấp nhận các trạng thái kém hơn) và giảm dần nhiệt độ theo thời gian. Khi nhiệt độ cao, thuật toán có thể chấp nhận bước di chuyển tệ hơn để thoát khỏi cực trị cục bộ. Khi nhiệt độ giảm, thuật toán chỉ chấp nhận các bước cải thiện.
- **Công thức xác suất chấp nhận bước tệ hơn:**  
\[
P = e^{-\Delta E / T}
\]
  - Trong đó:  
  - \( \Delta E = E_{\text{next}} - E_{\text{current}} \) là sự thay đổi năng lượng (hoặc chi phí).  
  - \( T \) là nhiệt độ hiện tại.  
  - \( P \) là xác suất chấp nhận bước tệ hơn.
- **Ưu điểm:** Có khả năng thoát khỏi cực trị cục bộ mà Hill Climbing mắc phải. Thường tìm được lời giải tốt hơn Hill Climbing trong không gian trạng thái lớn.
- **Nhược điểm:** Tốc độ chậm hơn các thuật toán, kết quả phụ thuộc mạnh vào các tham số.

#### 3. Tìm Kiếm Beam (Beam Search)
- **Nguyên lý:** Beam Search là biến thể của Breadth-First Search nhưng giới hạn số lượng trạng thái mở rộng tại mỗi mức (beam width = k). Thuật toán chỉ giữ k trạng thái tốt nhất theo hàm heuristic tại mỗi bước. Các trạng thái còn lại bị loại bỏ
- **Ưu điểm:** Giảm đáng kể bộ nhớ và số trạng thái cần xét so với BFS, giảm nguy cơ kẹt trong local maximum. Hiệu quả với không gian trạng thái lớn.   
- **Nhược điểm:**  Không đảm bảo tìm được lời giải tối ưu, vì các trạng thái tốt có thể bị loại bỏ sớm.  

#### 4. Thuật Toán Di Truyền (Genetic Algorithm – GA)
- **Nguyên lý:** Genetic Algorithm mô phỏng quá trình tiến hóa sinh học để tìm lời giải tối ưu.
  1. **Khởi tạo**: Tạo quần thể ban đầu gồm nhiều cá thể (trạng thái khả thi).  
  2. **Đánh giá**: Sử dụng **hàm fitness** để đánh giá chất lượng từng cá thể.  
  3. **Chọn lọc (Selection)**: Chọn các cá thể tốt hơn để làm cha mẹ.  
  4. **Crossover**: Kết hợp các cá thể cha mẹ để tạo ra thế hệ con.  
  5. **Mutation**: Thay đổi ngẫu nhiên một số gene để duy trì tính đa dạng.  
  6. **Lặp lại** các bước trên cho đến khi đạt điều kiện dừng (số thế hệ, fitness đạt chuẩn, hoặc tìm được lời giải tối ưu).  
- **Ưu điểm:**  Thích hợp cho không gian trạng thái lớn và phức tạp, khám phá toàn cục.
- **Nhược điểm:**  tham số kích thước quần thể, xác suất crossover, mutation rate, số thế hệ cần phù hợp. Tốn thời gian cho các quần thể lớn.  

### Thuật toán tìm kiếm trong môi trường phức tạp
#### 1. And-Or Search
- **Nguyên lý:** And-Or Search được sử dụng trong môi trường không chắc chắn hoặc **có hành động kết hợp (and/or). **OR nodes**: Chọn một trong các hành động khả thi để đạt mục tiêu. **AND nodes**: Tất cả các hành động con đều phải thành công để đạt mục tiêu.   
- **Ưu điểm:** Thích hợp cho **môi trường có nhiều kết quả ngẫu nhiên** (stochastic environment).  
- **Nhược điểm:** Tốn bộ nhớ và thời gian khi không gian trạng thái lớn.
- 
#### 2. Belief State Search
- **Nguyên lý:** Belief State Search được dùng khi môi trường không chắc chắn hoặc thông tin bị giới hạn. Thuật toán lưu tập hợp các trạng thái có thể xảy ra (belief state). Khi thực hiện một hành động, belief state được cập nhật. Thuật toán mở rộng tập hợp các belief state để tìm kiếm trạng thái mục tiêu.
- **Ưu điểm:** Thích hợp cho môi trường không quan sát được thông tin. 
- **Nhược điểm:**  Không gian belief state rất lớn, tốn bộ nhớ và thời gian. Cần cập nhật belief state sau mỗi hành động.
- 
#### 3. Partially Observable Search
- **Nguyên lý:** Partially Observable Search được sử dụng khi môi trường chỉ quan sát được một phần thông tin (partial observability). Trạng thái thực tế có thể không biết đầy đủ. Thuật toán duy trì tập hợp các trạng thái belief states dựa trên thông tin được biết một phần.
- **Ưu điểm:** Phù hợp cho môi trường thông tin không đầy đủ.
- **Nhược điểm:** Tốn bộ nhớ và tài nguyên tính toán do phải quản lý tập hợp các trạng thái belief state.

### Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problem)
#### 1. Quay Lui (Backtracking)
- **Nguyên lý:** Duyệt không gian trạng thái theo chiều sâu, gán giá trị cho từng biến. Khi một ràng buộc bị vi phạm, thuật toán quay lui (backtrack) để thử giá trị khác.  
- **Ưu điểm:** Dễ cài đặt.     
- **Nhược điểm:** Khi không gian trạng thái lớn thì tốn nhiều bộ nhớ và thời gian.
- 
#### 2. Forward Checking
- **Nguyên lý:** Khi gán giá trị cho một biến, thuật toán kiểm tra trước (forward) các biến chưa gán, loại bỏ các giá trị trong miền của biến còn lại mà **sẽ gây vi phạm ràng buộc**. Nếu một biến chưa gán không còn giá trị hợp lệ, thuật toán quay lui ngay thay vì tiếp tục duyệt sâu.  
- **Ưu điểm:** Giảm số nhánh phải thử so với Backtracking. Phát hiện vi phạm ràng buộc giúp giảm thời gian  
- **Nhược điểm:** Cần tính toán và cập nhật miền giá trị liên tục
- 
#### 3. Arc Consistency (AC-3)
- **Nguyên lý:** Mỗi arc (Xi, Xj) được coi là consistent nếu mọi giá trị của Xi có ít nhất một giá trị hợp lệ tương ứng trong Xj.
  - Thuật toán lặp đi lặp lại:  
    1. Lấy một arc (Xi, Xj) từ hàng đợi.  
    2. Loại bỏ các giá trị của Xi **không có giá trị hợp lệ tương ứng trong Xj**.  
    3. Nếu có thay đổi, thêm lại các arc liên quan đến Xi vào hàng đợi. Quá trình lặp lại đến khi không còn giá trị nào cần loại bỏ.
- **Ưu điểm:** Giảm miền giá trị trước khi hoặc trong quá trình Backtracking. Giúp phát hiện các trạng thái không có nghiệm thỏa mãn 
- **Nhược điểm:**  AC-3 không đảm bảo tìm lời giải, chỉ lọc giá trị không hợp lệ.  

## CÁC HÀM TÍNH CHI PHÍ
### Hàm đánh giá chi phí thực tế: `manhattan_chain_cost(board)`
1. Lấy danh sách các quân Rook trên bàn cờ (board), đồng thời ghi nhận các hàng đã có quân.  
2. Tính tổng khoảng cách Manhattan giữa các quân Rook theo thứ tự xuất hiện:  
   \[
   \text{cost} = \sum_{i=1}^{k-1} \big( |r_i - r_{i+1}| + |c_i - c_{i+1}| \big)
   \]  
   với \( (r_i, c_i) \) là tọa độ quân thứ i.
### Hàm đánh giá khoảng cách: `manhattan_distance_rooks(board, target)`
1. Duyệt từng **hàng của bàn cờ**.  
2. Nếu hàng có quân Rook, lấy **cột hiện tại** và **cột mục tiêu**.  
3. Tính khoảng cách Manhattan trên hàng so với mục tiêu:  
   \[
   \text{distance} = \sum_{r=0}^{N-1} |c_{\text{current}} - c_{\text{target}}|
   \]  
4. Tổng tất cả các khoảng cách để ra chi phí heuristic.

## SO SÁNH HIỆU SUẤT
### Thuật toán không có thông tin
[
### Thuật toán có thông tin
### Thuật toán tìm kiếm cục bộ
### Thuật toán tìm kiếm CSP
### Thuật toán tìm kiếm trong môi trường phức tạp

