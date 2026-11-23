# ADR 0001 — Sinh tham chiếu skill từ dữ liệu nguồn

**Trạng thái** · Đã áp dụng

**Ngày ghi nhận** · 2026-11-24

## Bối cảnh

Dữ liệu Garena được cập nhật theo phiên bản, ảnh trong client bổ sung các trường Học viện thiếu, còn nhận định chiến thuật thay đổi sau thực chiến. Cùng một cơ chế có thể phục vụ cả tra cứu, cấm/chọn và hướng dẫn lối chơi. Các skill cần đủ tài liệu để đóng gói riêng cho từng agent.

## Quyết định

Duy trì snapshot Garena trong `data/raw_official/`, dữ liệu client trong `data/ingame_stats/` và phần chiến thuật trong `data/tactical/`. Dùng slug chính thức để nối các nguồn. Compiler tạo Markdown trong `data/compiled/` và phân phối các tệp cần thiết vào `skills/*/references/`. Repo lưu các tham chiếu đã sinh để có thể dùng ngay sau khi clone và để review thay đổi dữ liệu trong Git.

Bản vá áp dụng mới nhất được ưu tiên khi có xung đột với mô tả Học viện. Dữ liệu chép từ client và quan sát thực chiến có ghi nguồn riêng để người duyệt biết chi tiết nào còn cần đối chiếu.

## Phương án từng cân nhắc

- Duy trì tham chiếu riêng trong mỗi skill giúp chỉnh nhanh một gói, nhưng dễ khiến các skill đưa ra số liệu khác nhau cho cùng câu hỏi.
- Đọc trực tiếp JSON trong repo tránh lưu đầu ra, nhưng làm các gói skill độc lập phụ thuộc vào bố cục repo và khó sử dụng trên Gemini Web hơn.

## Hệ quả

Mọi sửa đổi dữ liệu cần đi từ tệp nguồn và chạy lại compiler. Khi bản vá ra, có thể đồng bộ snapshot mà vẫn lưu được ảnh và kiến thức chiến thuật đã duyệt. Mỗi gói tải lên Gemini giữ một snapshot tại thời điểm tạo ZIP và cần được nạp lại khi tham chiếu cập nhật.
