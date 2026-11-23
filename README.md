# AthanorLab

AthanorLab là bộ **AI coach cho Liên Quân Mobile (Arena of Valor), máy chủ Việt Nam**. Sáu Agent Skills giúp bạn tra cứu dữ liệu game, chọn tướng, đổi hướng lên đồ và ra quyết định trong trận. Kho dữ liệu kết hợp Học viện Garena, ghi chú bản vá, ảnh trong client và hồ sơ chiến thuật đã duyệt.

Khi phát hành Batch 01, AthanorLab có **130 hồ sơ chỉ số trong client và 17 hồ sơ chiến thuật đã duyệt**. Xem ngày bản vá và phạm vi dữ liệu hiện hành trong [manifest](data/compiled/data_manifest.md).

## Dùng ngay

### Gemini Web

1. Mở **Customize → Skills → Create → Upload**.
2. Tải cả thư mục của skill bạn muốn dùng. Nếu dùng ZIP, nén từ bên trong thư mục để `SKILL.md` nằm ở gốc ZIP và giữ nguyên đường dẫn `references/`.
3. Trong chat mới, gõ `/` hoặc `@` tùy giao diện rồi chọn skill. Bắt đầu với **Lối chơi** và **Tra cứu**. Khi dữ liệu được cập nhật, dùng **Replace skill** để nạp lại gói. [Hướng dẫn Gemini Apps](https://support.google.com/gemini/answer/17094296?hl=en)

### Agent chạy trong repo

Clone repo bằng tài khoản GitHub có quyền truy cập.

```bash
git clone https://github.com/minhkhang1008/AthanorLab.git
cd AthanorLab
```

Mở thư mục trong agent và chỉ rõ skill muốn dùng từ bảng bên dưới. Với Gemini CLI, chạy hai lệnh sau từ thư mục repo và xác nhận liên kết khi được hỏi. [Hướng dẫn Agent Skills của Gemini CLI](https://geminicli.com/docs/cli/using-agent-skills/)

```bash
gemini skills link ./skills --scope workspace
gemini
```

Trong Gemini CLI, chọn tin cậy thư mục AthanorLab khi được hỏi rồi dùng `/skills list` để kiểm tra. Nếu skill chưa hiện, chạy `/trust` và mở lại phiên. [Hướng dẫn về thư mục tin cậy](https://geminicli.com/docs/cli/trusted-folders/)

| Nhu cầu | Skill |
| --- | --- |
| Chiêu thức, chỉ số, giá đồ, ngọc, phụ hiệu và phụ trợ | [aov-data-lookup](skills/aov-data-lookup/SKILL.md) |
| Cấm/chọn, phân tích đội hình, tìm tướng theo bể tướng | [aov-draft-coach](skills/aov-draft-coach/SKILL.md) |
| Mua món hoặc mảnh tiếp theo, đổi đồ theo thế trận | [aov-build-coach](skills/aov-build-coach/SKILL.md) |
| Trao đổi chiêu, giữ vị trí, tranh mục tiêu và giao tranh | [aov-gameplay-coach](skills/aov-gameplay-coach/SKILL.md) |
| So sánh thay đổi cân bằng và tác động của bản vá | [aov-patch-analyst](skills/aov-patch-analyst/SKILL.md) |
| Đồng bộ nguồn, nhập ảnh client và áp dụng hồ sơ đã duyệt trong repo | [aov-sync-maintainer](skills/aov-sync-maintainer/SKILL.md) |

### Hỏi theo tình huống

> Tôi chơi **Dyadia trợ thủ**, cấp 5, có 480 vàng nội tại. Y’bneth còn Chiêu 2, Xạ thủ mình đang đẩy cao và hai đội sắp tranh Rồng. Cho tôi vị trí đứng, chiêu nên dùng trước và tín hiệu để lao vào hoặc rút. Nếu mô tả Học viện khác ghi chú Batch 01, ghi rõ nguồn cho nhận định đó.

Khi cần trả lời nhanh, gửi **tướng, cấp, đồ đang có, chênh lệch vàng, mối đe dọa và quyết định cần ngay**. Khi cấm/chọn, gửi các lượt đã khóa, vị trí còn thiếu và bể tướng bạn chơi được.

## Cách AthanorLab xử lý dữ liệu

```text
Học viện + bản vá Garena   → data/raw_official/
Ảnh bảng Thuộc tính       → data/ingame_stats/
Ghi chú thực chiến đã duyệt → data/tactical/
                             ↓ compiler.build_all
                  data/compiled/ và skills/*/references/
```

- **Bản vá và Học viện.** Khi bản vá sửa đúng cơ chế hoặc thông số đang tra, dùng bản vá mới nhất áp dụng cho thay đổi đó. Xem thêm [chỉ mục bản vá](data/compiled/patch_history_index.md).
- **Dữ liệu client.** Hồ sơ giữ các chỉ số nhìn thấy trên bảng Thuộc tính. Hệ số chiêu và trường bị thiếu cần ảnh chi tiết hoặc ghi chú bản vá để xác nhận.
- **Nhận định chiến thuật.** Điểm Early/Mid/Late phụ thuộc vai trò, trang bị và trạng thái trận, có thể thay đổi sau khi thử nghiệm. [Batch 01](data/tactical/curated_batches/batch_01.json) ghi rõ nguồn cho các nhận định và các cơ chế đang chờ đối chiếu thêm.

## Chạy và bảo trì ở máy local

GitHub Actions dùng Python 3.11. Dùng phiên bản này để tái tạo quy trình kiểm tra.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m compiler.build_all
```

| Lệnh chạy từ gốc repo | Mục đích |
| --- | --- |
| `python skills/aov-data-lookup/scripts/query_aov.py hero evita` | Tra nhanh mô tả Học viện trong snapshot chính thức |
| `python skills/aov-data-lookup/scripts/query_aov.py item "chuy bang"` | Tra giá, chỉ số và nội tại trang bị |
| `python skills/aov-data-lookup/scripts/query_aov.py patch fennik` | Tìm dòng cân bằng theo tên tướng |
| `python -m scraper.validator` | Kiểm tra snapshot hiện có và ghi lại manifest |
| `python -m scraper.run_all --only patches --refresh --delay 0.5` | Tải và kiểm tra bản vá từ Garena |
| `python -m compiler.apply_curation` | Áp dụng các batch đã duyệt và biên dịch lại skill |

Xem [hướng dẫn đóng góp](CONTRIBUTING.md), [lịch sử thay đổi](CHANGELOG.md) và [quyết định tổ chức dữ liệu](docs/decisions/0001-generated-skill-references.md).
