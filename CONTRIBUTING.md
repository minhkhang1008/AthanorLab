# Đóng góp cho AthanorLab

## Báo sai dữ liệu hoặc góp ý chiến thuật

Dùng [mẫu báo cáo](.github/ISSUE_TEMPLATE/data-or-coaching.md). Ghi tên tướng hoặc slug, bản vá và phần trả lời cần sửa. Với sai lệch cơ chế, gửi URL bản vá hoặc ảnh kỹ năng trong client và che UID, tên tài khoản nếu xuất hiện. Với góp ý chiến thuật, ghi vai trò, cấp, trang bị, chênh lệch vàng, vị trí mục tiêu và quyết định nào sẽ thay đổi. Mô tả tình huống đủ cụ thể để người khác có thể thử lại.

## Chỉnh đúng tệp nguồn

| Nội dung | Vị trí |
| --- | --- |
| Dữ liệu lấy từ Garena | `scraper/` sinh `data/raw_official/` từ snapshot chính thức |
| Ảnh thuộc tính hoặc chi tiết kỹ năng | `data/ingame_stats/<slug>.json`, xem [hồ sơ mẫu](data/ingame_stats/_example_richter.json) |
| Hồ sơ chiến thuật chờ duyệt | `data/tactical/curated_batches/_batch_NN.json` |
| Hồ sơ đã duyệt | `data/tactical/curated_batches/batch_NN.json` |
| Khung nhịp trận, cấm/chọn và trang bị khắc chế | `data/tactical/` |
| Hướng dẫn hành vi của agent | `skills/<tên-skill>/SKILL.md` |

Dùng slug từ [chỉ mục tướng](data/compiled/heroes_index.md), kể cả khi cùng tên hiển thị như Flowborn. Giữ trường chưa quan sát được ở dạng trống hoặc bỏ trường. Ghi nguồn và phân biệt số liệu đã xác nhận với nhận định từ trải nghiệm chơi.

Sửa batch đã duyệt khi cập nhật một hồ sơ thuộc batch. Trình áp dụng đọc batch theo thứ tự tên tệp và có thể áp dụng lại nội dung đã lưu. Tệp có tên bắt đầu bằng `_` được bỏ qua. Sau khi duyệt bản nháp, bỏ dấu gạch dưới ở đầu tên và chạy:

```bash
python -m compiler.apply_curation
```

Khi chỉ chỉnh chỉ số client hoặc tài liệu chiến thuật ngoài batch, chạy:

```bash
python -m compiler.build_all
```

## Kiểm tra trước khi mở pull request

1. Nếu thay đổi scraper hoặc snapshot chính thức, chạy `python -m scraper.validator`. Kiểm tra `status`, `error_count` và mục cảnh báo trong [manifest thô](data/raw_official/manifest.json).
2. Chạy compiler sau lần chỉnh dữ liệu cuối. Kiểm tra cả [đầu ra chung](data/compiled) và thư mục `references/` của các skill liên quan.
3. Thử một câu hỏi có thể phát hiện lỗi cũ. Ghi đầu vào và quyết định đúng cần nhận được. Với dữ liệu kỹ năng xung đột, trích đúng nguồn và ngày của mỗi bên.
4. Chạy `git diff --check` và đưa các tệp nguồn cùng tham chiếu tái tạo vào PR. Giữ ảnh gốc, cache và các bản chat làm việc ở local.

Workflow [Sync Official AoV Data & Compile Skills](.github/workflows/sync-patch.yml) chạy theo lịch hoặc theo yêu cầu để lấy dữ liệu Garena, kiểm tra, biên dịch và mở PR khi đầu ra thay đổi. Khi review PR bản vá, rà lại hồ sơ của các tướng bị làm lại hoặc bị đổi ngưỡng sức mạnh.
