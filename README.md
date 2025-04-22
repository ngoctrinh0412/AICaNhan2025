# Đồ án AI cá nhân: 8-Puzzle

## Giới thiệu

Đồ án này triển khai các thuật toán trí tuệ nhân tạo (AI) để giải quyết bài toán 8-Puzzle Problem. 8-Puzzle là một trò chơi xếp số trên bảng 3x3, gồm 8 ô số (từ 1 đến 8) và 1 ô trống (zero). Mục tiêu là di chuyển ô trống (lên, xuống, trái, phải) để đưa trạng thái ban đầu về trạng thái đích (goal state).

Dự án sử dụng nhiều thuật toán AI, chia thành các nhóm: Uninformed Search, Informed Search, Local Search, Genetic Algorithm, AND-OR Search, và Belief State Search. Các thuật toán được triển khai để tìm đường đi từ trạng thái ban đầu đến trạng thái đích, đồng thời so sánh hiệu quả giữa chúng.

Code được viết bằng Python, sử dụng các thư viện như pygame (cho giao diện GUI), numpy, và các hàm tiện ích trong utils.py để xử lý trạng thái, tính khoảng cách Manhattan, và tạo trạng thái niềm tin.

## Các nhóm thuật toán

### Uninformed Search (Tìm kiếm không có thông tin)

Các thuật toán này không sử dụng thông tin heuristic, chỉ dựa vào cấu trúc của không gian trạng thái:

BFS (Breadth-First Search): Tìm kiếm theo chiều rộng.
DFS (Depth-First Search): Tìm kiếm theo chiều sâu.
IDS (Iterative Deepening Search): Tìm kiếm lặp sâu dần.
UCS (Uniform Cost Search): Tìm kiếm chi phí đồng nhất.

So sánh:

BFS và IDS tìm được đường ngắn nhất, nhưng BFS tốn nhiều bộ nhớ hơn (O(b^d)).
DFS nhanh nhưng không hoàn chỉnh, có thể không tìm được lời giải nếu không giới hạn độ sâu.
UCS tối ưu nhưng tốn bộ nhớ tương tự BFS.

Kết quả thực tế :

### Informed Search (Tìm kiếm có thông tin)

Các thuật toán này sử dụng heuristic (khoảng cách Manhattan) để định hướng tìm kiếm:

Greedy Search: Tìm kiếm tham lam.
A Search*: Tìm kiếm A*.
IDA (Iterative Deepening A)\*_: Tìm kiếm A_ lặp sâu dần.
Beam Search: Tìm kiếm chùm (beam width = 3).

So sánh:

A* và IDA* tối ưu, nhưng A* tốn bộ nhớ hơn (O(b^d)), còn IDA* tiết kiệm bộ nhớ.
Greedy nhanh nhưng không tối ưu, có thể bỏ sót lời giải.
Beam Search nhanh, tiết kiệm bộ nhớ, nhưng không hoàn chỉnh (có thể bỏ sót lời giải).

Kết quả thực tế:

### Local Search (Tìm kiếm cục bộ)

Các thuật toán này tập trung vào cải thiện từng bước, không đảm bảo tìm lời giải tối ưu:

Simple Hill Climbing: Leo đồi đơn giản.
Steepest-Ascent Hill Climbing: Leo đồi dốc nhất.
Stochastic Hill Climbing: Leo đồi ngẫu nhiên.
Simulated Annealing: Ủ kim loại mô phỏng.

So sánh:

Simple và Steepest-Ascent dễ bị kẹt ở cực trị cục bộ.
Stochastic thêm yếu tố ngẫu nhiên, có thể thoát cực trị cục bộ nhưng không đảm bảo lời giải.
Simulated Annealing hiệu quả hơn nhờ cơ chế nhiệt độ, có khả năng thoát cực trị cục bộ.

Kết quả thực tế:

### Genetic Algorithm (Thuật toán di truyền)

Genetic Algorithm: Tạo quần thể các đường đi, tiến hành lai ghép và đột biến để tìm lời giải.

So sánh:

Phù hợp với không gian tìm kiếm lớn, nhưng phụ thuộc vào tham số (population size, mutation rate).
Không đảm bảo lời giải tối ưu, nhưng có thể tìm đường đi khả thi.

Kết quả thực tế:

### AND-OR Search

AND-OR Search: Tìm kiếm dạng cây AND-OR, phù hợp với bài toán có nhiều lựa chọn.

So sánh:

Hữu ích khi có nhiều lựa chọn, nhưng phức tạp và tốn tài nguyên nếu không giới hạn độ sâu.

Kết quả thực tế:

### Belief State Search

Belief State Search: Tìm kiếm dựa trên trạng thái niềm tin, xử lý bài toán với thông tin đầy đủ và không đầy đủ.

Hai trường hợp:

Trường hợp đầy đủ thông tin (Full State):

Mô tả: Trạng thái ban đầu được biết hoàn toàn (không có ô nào là None). Thuật toán tạo một tập belief states duy nhất (chỉ chứa trạng thái ban đầu) và tìm kiếm đường đi đến trạng thái đích bằng A\* Search.
Ưu điểm: Đơn giản, nhanh, ít tốn bộ nhớ (chỉ có 1 belief state).
Nhược điểm: Không tận dụng được đặc trưng của Belief State Search, vì không có thông tin không đầy đủ.

Trường hợp không đầy đủ thông tin (Partial State):

Mô tả: Trạng thái ban đầu có một số ô không biết (None). Thuật toán tạo tập belief states chứa tất cả trạng thái khả thi, dựa trên các ô đã biết và trạng thái đích, rồi tìm kiếm đường đi bằng A\* Search.
Ưu điểm: Hữu ích khi xử lý thông tin không đầy đủ, mô phỏng tình huống thực tế (như robot di chuyển trong môi trường không biết trước).
Nhược điểm: Phức tạp, tốn tài nguyên do phải duy trì và cập nhật nhiều trạng thái niềm tin (số lượng belief states có thể lớn).

So sánh:

Độ phức tạp: Full State đơn giản hơn (O(b^d)), trong khi Partial State phức tạp hơn (O(b^d \* |B|), với |B| là số belief states).
Hiệu quả: Full State nhanh và ít tốn bộ nhớ, nhưng không thể hiện ưu điểm của Belief State Search. Partial State chậm hơn, tốn bộ nhớ, nhưng phù hợp với bài toán thực tế.
Khả năng áp dụng: Full State chỉ phù hợp khi biết hết trạng thái, còn Partial State phù hợp với bài toán có thông tin không đầy đủ.

Kết quả thực tế:

## Ảnh kết quả

Dưới đây là ảnh chụp giao diện GUI và kết quả của các thuật toán:

Giao diện GUI:

Biểu đồ so sánh số bước:

## Hướng dẫn cài đặt và chạy

- Cài đặt pygame: 'pip install pygame'
- Cài đặt numpy để xử lý mảng và tính toán: 'pip install numpy'
- Chạy: 'python gui.py'
