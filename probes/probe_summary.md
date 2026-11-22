# AthanorLab - Phase 1 Probe Summary
- **Generated (UTC):** `2026-11-22T19:55:23.121042+00:00`

## 1. WordPress API & Sitemap Check
| Endpoint | Status | Bytes | Note |
| :--- | :---: | :---: | :--- |
| `sitemap_index` | `200` | `1188` | XML <loc> count=7 | first=['https://lienquan.garena.vn/post-sitemap.xml', 'https://lienquan.garena.vn/page-sitemap.xml', 'https://lienquan.garena.vn/heroes-sitemap.xml'] |
| `sitemap_xml` | `200` | `1188` | XML <loc> count=7 | first=['https://lienquan.garena.vn/post-sitemap.xml', 'https://lienquan.garena.vn/page-sitemap.xml', 'https://lienquan.garena.vn/heroes-sitemap.xml'] |
| `wp_types` | `403` | `548` |  |
| `wp_categories` | `403` | `548` |  |
| `wp_posts_sample` | `403` | `548` |  |

## 2. Target Pages Overview
| Key | Status | Bytes | Blocked? | Server/CF Headers |
| :--- | :---: | :---: | :---: | :--- |
| `heroes_list` | `200` | `109505` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `hero_evita` | `200` | `43053` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `hero_flowborn_1` | `200` | `44111` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `hero_flowborn_2` | `200` | `44026` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `items` | `200` | `176549` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `arcana` | `200` | `111881` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `talents` | `200` | `43822` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `enchantments` | `200` | `78073` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |
| `updates` | `200` | `47316` | `False` | `content-type=text/html; charset=UTF-8, server=APISIX/3.17.0` |

## 3.heroes_list (`https://lienquan.garena.vn/hoc-vien/tuong-skin/`)
```json
{
  "total_hero_links": 130,
  "sample_heroes": [
    {
      "slug": "evita",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/evita/",
      "text": "Evita",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "evita",
        "data-type": "[29]",
        "data-tag": ""
      }
    },
    {
      "slug": "tamyn",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/tamyn/",
      "text": "Tamyn",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "tamyn",
        "data-type": "[28]",
        "data-tag": ""
      }
    },
    {
      "slug": "flowborn-2",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn-2/",
      "text": "Flowborn",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "flowborn",
        "data-type": "[29]",
        "data-tag": ""
      }
    },
    {
      "slug": "flowborn",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn/",
      "text": "Flowborn",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "flowborn",
        "data-type": "[33]",
        "data-tag": ""
      }
    },
    {
      "slug": "dyadia",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/dyadia/",
      "text": "Dyadia",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "dyadia",
        "data-type": "[30]",
        "data-tag": ""
      }
    }
  ],
  "duplicate_display_names": {
    "Flowborn": [
      "flowborn-2",
      "flowborn"
    ]
  },
  "has_evita": true,
  "flowborn_slugs": [
    {
      "slug": "flowborn-2",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn-2/",
      "text": "Flowborn",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "flowborn",
        "data-type": "[29]",
        "data-tag": ""
      }
    },
    {
      "slug": "flowborn",
      "url": "https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn/",
      "text": "Flowborn",
      "a_class": "st-heroes__item",
      "parent_tag": "div",
      "parent_class": "st-heroes__list",
      "data_attrs": {
        "data-keyword": "flowborn",
        "data-type": "[33]",
        "data-tag": ""
      }
    }
  ],
  "role_filters": [
    {
      "tag": "a",
      "class": [
        "st-heroes__item"
      ],
      "text": "Evita",
      "data": {
        "data-keyword": "evita",
        "data-type": "[29]",
        "data-tag": ""
      }
    },
    {
      "tag": "a",
      "class": [
        "st-heroes__item"
      ],
      "text": "Tamyn",
      "data": {
        "data-keyword": "tamyn",
        "data-type": "[28]",
        "data-tag": ""
      }
    },
    {
      "tag": "a",
      "class": [
        "st-heroes__item"
      ],
      "text": "Flowborn",
      "data": {
        "data-keyword": "flowborn",
        "data-type": "[29]",
        "data-tag": ""
      }
    },
    {
      "tag": "a",
      "class": [
        "st-heroes__item"
      ],
      "text": "Flowborn",
      "data": {
   
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.hero_evita (`https://lienquan.garena.vn/hoc-vien/tuong-skin/d/evita/`)
```json
{
  "title": "Evita | Liên Quân Mobile",
  "headings": [
    {
      "tag": "h1",
      "class": [
        "p-academy__title",
        "title"
      ],
      "text": "Gameplay"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Evita"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skins--title"
      ],
      "text": "Trang phục"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skills--title"
      ],
      "text": "Kỹ năng"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Ma lực hắc ám"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Bộc phá hắc ám"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Quyền lực hắc ám"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Triệu hồi hắc ám"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "CÔNG TY CỔ PHẦN GIẢI TRÍ VÀ THỂ THAO ĐIỆN TỬ VIỆT NAM"
    }
  ],
  "skill_block_candidates": [
    {
      "selector": "div#.hero",
      "text_preview": "Evita Trang phục Kỹ năng Ma lực hắc ám Evita sẽ chuyển hóa Ma lực hắc ám theo thời gian. Khi tích đầy ma lực, lần kế tiếp tung chiêu trúng mục tiêu sẽ tiêu hao toàn bộ ma lực khiến Ma vật hỗn mang lao tới mục tiêu gây sát thương phép đồng thời giúp bản thân nhận lá chắn Bộc phá hắc ám Evita thả Ma vật hỗn mang hướng về phía chỉ định. Khi trúng kẻ đ\n... [TRUNCATED]",
      "html_preview": "<div class=\"hero\">\n <!-- SKINS -->\n <section class=\"hero__skins\">\n  <div class=\"hero__skins--detail active\" id=\"heroSkin-1\">\n   <h3>\n    Evita\n   </h3>\n   <picture>\n    <img src=\"https://lienquan.garena.vn/wp-content/uploads/2026/10/SeaTalk_IMG_20261014_172710-1.jpeg\"/>\n   </picture>\n  </div>\n  <h2 class=\"hero__skins--title\">\n   Trang phục\n  </h2>\n  <ul class=\"hero__skins--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkin-1\" title=\"Evita\">\n     <img alt=\"Evita\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/10/avt.jpeg\"/>\n    </a>\n   </li>\n  </ul>\n </section>\n <!-- SKILLS -->\n <section class=\"hero__skills\">\n  <h2 class=\"hero__skills--title\">\n   Kỹ năng\n  </h2>\n  <div class=\"hero__skills--main\">\n   <ul class=\"hero__skills--list\">\n    <li>\n     <a class=\"active\" href=\"#heroSkill-1\" title=\"Ma lực hắc ám\">\n      <img alt=\"Ma lực hắc ám\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/10/SeaTalk_IMG_20261014_172717-1.png\"/>\n     </a>\n    </li>\n    <li>\n     <a class=\"\" href=\"#heroSkill-2\" title=\"Bộc phá hắc ám\">\n      <img alt=\"Bộc phá hắc ám\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/10/SeaTalk_IMG_20261014_172732.png\"/>\n     </a>\n    </li>\n    <li>\n  \n... [TRUNCATED]"
    },
    {
      "selector": "section#.hero__skills",
      "text_preview": "Kỹ năng Ma lực hắc ám Evita sẽ chuyển hóa Ma lực hắc ám theo thời gian. Khi tích đầy ma lực, lần kế tiếp tung chiêu trúng mục tiêu sẽ tiêu hao toàn bộ ma lực khiến Ma vật hỗn mang lao tới mục tiêu gây sát thương phép đồng thời giúp bản thân nhận lá chắn Bộc phá hắc ám Evita thả Ma vật hỗn mang hướng về phía chỉ định. Khi trúng kẻ địch hoặc bay đến \n... [TRUNCATED]",
      "html_preview": "<section class=\"hero__skills\">\n <h2 class=\"hero__skills--title\">\n  Kỹ năng\n </h2>\n <div class=\"hero__skills--main\">\n  <ul class=\"hero__skills--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkill-1\" title=\"Ma lực hắc ám\">\n     <img alt=\"Ma lực hắc ám\" src=\"https://lien
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.hero_flowborn_1 (`https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn/`)
```json
{
  "title": "Flowborn | Liên Quân Mobile",
  "headings": [
    {
      "tag": "h1",
      "class": [
        "p-academy__title",
        "title"
      ],
      "text": "Gameplay"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Flowborn"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skins--title"
      ],
      "text": "Trang phục"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skills--title"
      ],
      "text": "Kỹ năng"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy năng lượng"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy hội tụ"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Nỏ tiễn phá không"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Nỏ tiễn liên hoàn"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "CÔNG TY CỔ PHẦN GIẢI TRÍ VÀ THỂ THAO ĐIỆN TỬ VIỆT NAM"
    }
  ],
  "skill_block_candidates": [
    {
      "selector": "div#.hero",
      "text_preview": "Flowborn Trang phục Kỹ năng Dòng chảy năng lượng Nội tại: Flowborn tại tế đàn có thể dẫn “Dòng chảy” vào cơ thể để tôi luyện bản thân, nhận Tốc đánh và cường hóa một trong bốn thuộc tính sau: Sinh mệnh: Nhận thêm Máu tối đa Xuyên phá: Nhận thêm Công vật lý Gia Tốc: Nhận thêm Tốc chạy Tĩnh tâm: Nhận thêm Giảm hồi chiêu Đòn đánh thường cường hóa: Phó\n... [TRUNCATED]",
      "html_preview": "<div class=\"hero\">\n <!-- SKINS -->\n <section class=\"hero__skins\">\n  <div class=\"hero__skins--detail active\" id=\"heroSkin-1\">\n   <h3>\n    Flowborn\n   </h3>\n   <picture>\n    <img src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20260403_100333.jpg\"/>\n   </picture>\n  </div>\n  <h2 class=\"hero__skins--title\">\n   Trang phục\n  </h2>\n  <ul class=\"hero__skins--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkin-1\" title=\"Flowborn\">\n     <img alt=\"Flowborn\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/IMG-SQR-0150x0150-080151-ket-thuc2.jpg\"/>\n    </a>\n   </li>\n  </ul>\n </section>\n <!-- SKILLS -->\n <section class=\"hero__skills\">\n  <h2 class=\"hero__skills--title\">\n   Kỹ năng\n  </h2>\n  <div class=\"hero__skills--main\">\n   <ul class=\"hero__skills--list\">\n    <li>\n     <a class=\"active\" href=\"#heroSkill-1\" title=\"Dòng chảy năng lượng\">\n      <img alt=\"Dòng chảy năng lượng\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20260403_103402.png\"/>\n     </a>\n    </li>\n    <li>\n     <a class=\"\" href=\"#heroSkill-2\" title=\"Dòng chảy hội tụ\">\n      <img alt=\"Dòng chảy hội tụ\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20\n... [TRUNCATED]"
    },
    {
      "selector": "section#.hero__skills",
      "text_preview": "Kỹ năng Dòng chảy năng lượng Nội tại: Flowborn tại tế đàn có thể dẫn “Dòng chảy” vào cơ thể để tôi luyện bản thân, nhận Tốc đánh và cường hóa một trong bốn thuộc tính sau: Sinh mệnh: Nhận thêm Máu tối đa Xuyên phá: Nhận thêm Công vật lý Gia Tốc: Nhận thêm Tốc chạy Tĩnh tâm: Nhận thêm Giảm hồi chiêu Đòn đánh thường cường hóa: Phóng ra nỏ tiễn xuyên \n... [TRUNCATED]",
      "html_preview": "<section class=\"hero__skills\">\n <h2 class=\"hero__skills--title\">\n  Kỹ năng\n </h2>\n <div class=\"hero__skills--main\">\n  <ul class=\"hero__skills--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkill-1\" title=\"Dòng chảy năng lượng\">\n     <img alt=\"Dòng chảy năng 
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.hero_flowborn_2 (`https://lienquan.garena.vn/hoc-vien/tuong-skin/d/flowborn-2/`)
```json
{
  "title": "Flowborn | Liên Quân Mobile",
  "headings": [
    {
      "tag": "h1",
      "class": [
        "p-academy__title",
        "title"
      ],
      "text": "Gameplay"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Flowborn"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skins--title"
      ],
      "text": "Trang phục"
    },
    {
      "tag": "h2",
      "class": [
        "hero__skills--title"
      ],
      "text": "Kỹ năng"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy năng lượng"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy hội tụ"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy pháp trận"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "Dòng chảy hủy diệt"
    },
    {
      "tag": "h3",
      "class": [],
      "text": "CÔNG TY CỔ PHẦN GIẢI TRÍ VÀ THỂ THAO ĐIỆN TỬ VIỆT NAM"
    }
  ],
  "skill_block_candidates": [
    {
      "selector": "div#.hero",
      "text_preview": "Flowborn Trang phục Kỹ năng Dòng chảy năng lượng Flowborn khi ở trong tế đàn có thể dẫn “Dòng chảy” vào cơ thể để tôi luyện bản thân, nhận công phép (tăng theo cấp tướng) và cường hóa một trong bốn thuộc tính sau: Sinh mệnh: Nhận thêm máu tối đa Xuyên phá: Nhận thêm xuyên giáp phép Gia tốc: Nhận thêm tốc chạy Tĩnh tâm: Nhận thêm giảm hồi chiêu Có t\n... [TRUNCATED]",
      "html_preview": "<div class=\"hero\">\n <!-- SKINS -->\n <section class=\"hero__skins\">\n  <div class=\"hero__skins--detail active\" id=\"heroSkin-1\">\n   <h3>\n    Flowborn\n   </h3>\n   <picture>\n    <img src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20260403_100333.jpg\"/>\n   </picture>\n  </div>\n  <h2 class=\"hero__skins--title\">\n   Trang phục\n  </h2>\n  <ul class=\"hero__skins--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkin-1\" title=\"Flowborn\">\n     <img alt=\"Flowborn\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/IMG-SQR-0150x0150-080149-22.jpg\"/>\n    </a>\n   </li>\n  </ul>\n </section>\n <!-- SKILLS -->\n <section class=\"hero__skills\">\n  <h2 class=\"hero__skills--title\">\n   Kỹ năng\n  </h2>\n  <div class=\"hero__skills--main\">\n   <ul class=\"hero__skills--list\">\n    <li>\n     <a class=\"active\" href=\"#heroSkill-1\" title=\"Dòng chảy năng lượng\">\n      <img alt=\"Dòng chảy năng lượng\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20260403_103402.png\"/>\n     </a>\n    </li>\n    <li>\n     <a class=\"\" href=\"#heroSkill-2\" title=\"Dòng chảy hội tụ\">\n      <img alt=\"Dòng chảy hội tụ\" src=\"https://lienquan.garena.vn/wp-content/uploads/2026/04/SeaTalk_IMG_20260403_\n... [TRUNCATED]"
    },
    {
      "selector": "section#.hero__skills",
      "text_preview": "Kỹ năng Dòng chảy năng lượng Flowborn khi ở trong tế đàn có thể dẫn “Dòng chảy” vào cơ thể để tôi luyện bản thân, nhận công phép (tăng theo cấp tướng) và cường hóa một trong bốn thuộc tính sau: Sinh mệnh: Nhận thêm máu tối đa Xuyên phá: Nhận thêm xuyên giáp phép Gia tốc: Nhận thêm tốc chạy Tĩnh tâm: Nhận thêm giảm hồi chiêu Có thể tiêu hao 1 tầng “\n... [TRUNCATED]",
      "html_preview": "<section class=\"hero__skills\">\n <h2 class=\"hero__skills--title\">\n  Kỹ năng\n </h2>\n <div class=\"hero__skills--main\">\n  <ul class=\"hero__skills--list\">\n   <li>\n    <a class=\"active\" href=\"#heroSkill-1\" title=\"Dòng chảy năng lượng\">\n     <img alt=\"Dòng chảy nă
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.items (`https://lienquan.garena.vn/hoc-vien/trang-bi/`)
```json
{
  "title": "Trang Bị | Liên Quân Mobile",
  "top_classes": [
    [
      "div.st-items__item",
      112
    ],
    [
      "div.st-items__item--img",
      112
    ],
    [
      "h2.st-items__item--name",
      112
    ],
    [
      "div.st-items__item--content",
      112
    ],
    [
      "li.menu-item",
      36
    ],
    [
      "li.menu-item-type-post_type",
      23
    ],
    [
      "li.menu-item-object-page",
      23
    ],
    [
      "li.menu-item-type-custom",
      13
    ],
    [
      "li.menu-item-object-custom",
      13
    ],
    [
      "li.menu-item-has-children",
      3
    ],
    [
      "ul.sub-menu",
      3
    ],
    [
      "li.current-menu-item",
      2
    ],
    [
      "li.page_item",
      2
    ],
    [
      "li.page-item-1700",
      2
    ],
    [
      "li.current_page_item",
      2
    ]
  ],
  "sample_items": [
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.current-menu-ancestor.current-menu-parent.current_page_parent.current_page_ancestor.menu-item-has-children.menu-item-1710",
      "text_preview": "Gameplay Tướng/Skin Trang Bị Bảng ngọc Phụ Trợ Phù Hiệu Chế độ chơi",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-ancestor current-menu-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-1710\" id=\"menu-item-1710\">\n <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-gameplay.png\"/>\n  <span>\n   Gameplay\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1709\" id=\"menu-item-1709\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n    Tướng/Skin\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-1700 current_page_item menu-item-1708\" id=\"menu-item-1708\">\n   <a aria-current=\"page\" href=\"https://lienquan.garena.vn/hoc-vien/trang-bi/\">\n    Trang Bị\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1704\" id=\"menu-item-1704\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/bang-ngoc/\">\n    Bảng ngọc\n   </a>\n  </li>\n  <li \n... [TRUNCATED]"
    },
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.menu-item-4468",
      "text_preview": "Tin tức Cập nhật Sự kiện Mở bán Hợp tác Giải đấu Cẩm nang",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-4468\" id=\"menu-item-4468\">\n <a href=\"https://lienquan.garena.vn/tin-tuc/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-news.png\"/>\n  <span>\n   Tin tức\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-224\" id=\"menu-item-224\">\n   <a href=\"https://lienquan.garena.vn/cap-nhat/\">\n    Cập nhật\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-228\" id=\"menu-item-228\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc/su-kien/\">\n    Sự kiện\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-227\" id=\"menu-item-227\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.arcana (`https://lienquan.garena.vn/hoc-vien/bang-ngoc/`)
```json
{
  "title": "Bảng ngọc | Liên Quân Mobile",
  "top_classes": [
    [
      "div.st-runes__item",
      88
    ],
    [
      "div.st-runes__item--img",
      88
    ],
    [
      "h2.st-runes__item--name",
      88
    ],
    [
      "div.st-runes__item--content",
      88
    ],
    [
      "li.menu-item",
      36
    ],
    [
      "li.menu-item-type-post_type",
      23
    ],
    [
      "li.menu-item-object-page",
      23
    ],
    [
      "li.menu-item-type-custom",
      13
    ],
    [
      "li.menu-item-object-custom",
      13
    ],
    [
      "li.menu-item-has-children",
      3
    ],
    [
      "ul.sub-menu",
      3
    ],
    [
      "li.current-menu-item",
      2
    ],
    [
      "li.page_item",
      2
    ],
    [
      "li.page-item-1692",
      2
    ],
    [
      "li.current_page_item",
      2
    ]
  ],
  "sample_items": [
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.current-menu-ancestor.current-menu-parent.current_page_parent.current_page_ancestor.menu-item-has-children.menu-item-1710",
      "text_preview": "Gameplay Tướng/Skin Trang Bị Bảng ngọc Phụ Trợ Phù Hiệu Chế độ chơi",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-ancestor current-menu-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-1710\" id=\"menu-item-1710\">\n <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-gameplay.png\"/>\n  <span>\n   Gameplay\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1709\" id=\"menu-item-1709\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n    Tướng/Skin\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1708\" id=\"menu-item-1708\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/trang-bi/\">\n    Trang Bị\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-item page_item page-item-1692 current_page_item menu-item-1704\" id=\"menu-item-1704\">\n   <a aria-current=\"page\" href=\"https://lienquan.garena.vn/hoc-vien/bang-ngoc/\">\n    Bảng ngọc\n   </a>\n  </li>\n  <li \n... [TRUNCATED]"
    },
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.menu-item-4468",
      "text_preview": "Tin tức Cập nhật Sự kiện Mở bán Hợp tác Giải đấu Cẩm nang",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-4468\" id=\"menu-item-4468\">\n <a href=\"https://lienquan.garena.vn/tin-tuc/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-news.png\"/>\n  <span>\n   Tin tức\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-224\" id=\"menu-item-224\">\n   <a href=\"https://lienquan.garena.vn/cap-nhat/\">\n    Cập nhật\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-228\" id=\"menu-item-228\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc/su-kien/\">\n    Sự kiện\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-227\" id=\"menu-item-227\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc/mo
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.talents (`https://lienquan.garena.vn/hoc-vien/phu-tro/`)
```json
{
  "title": "Phụ Trợ | Liên Quân Mobile",
  "top_classes": [
    [
      "li.menu-item",
      36
    ],
    [
      "li.menu-item-type-post_type",
      23
    ],
    [
      "li.menu-item-object-page",
      23
    ],
    [
      "li.menu-item-type-custom",
      13
    ],
    [
      "li.menu-item-object-custom",
      13
    ],
    [
      "div.st-extra-skills__item",
      9
    ],
    [
      "div.st-extra-skills__item--img",
      9
    ],
    [
      "h3.st-extra-skills__item--name",
      9
    ],
    [
      "div.st-extra-skills__item--content",
      9
    ],
    [
      "li.menu-item-has-children",
      3
    ],
    [
      "ul.sub-menu",
      3
    ],
    [
      "li.current-menu-item",
      2
    ],
    [
      "li.page_item",
      2
    ],
    [
      "li.page-item-1698",
      2
    ],
    [
      "li.current_page_item",
      2
    ]
  ],
  "sample_items": [
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.current-menu-ancestor.current-menu-parent.current_page_parent.current_page_ancestor.menu-item-has-children.menu-item-1710",
      "text_preview": "Gameplay Tướng/Skin Trang Bị Bảng ngọc Phụ Trợ Phù Hiệu Chế độ chơi",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-ancestor current-menu-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-1710\" id=\"menu-item-1710\">\n <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-gameplay.png\"/>\n  <span>\n   Gameplay\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1709\" id=\"menu-item-1709\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n    Tướng/Skin\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1708\" id=\"menu-item-1708\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/trang-bi/\">\n    Trang Bị\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1704\" id=\"menu-item-1704\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/bang-ngoc/\">\n    Bảng ngọc\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-item\n... [TRUNCATED]"
    },
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.menu-item-4468",
      "text_preview": "Tin tức Cập nhật Sự kiện Mở bán Hợp tác Giải đấu Cẩm nang",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-4468\" id=\"menu-item-4468\">\n <a href=\"https://lienquan.garena.vn/tin-tuc/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-news.png\"/>\n  <span>\n   Tin tức\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-224\" id=\"menu-item-224\">\n   <a href=\"https://lienquan.garena.vn/cap-nhat/\">\n    Cập nhật\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-228\" id=\"menu-item-228\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc/su-kien/\">\n    Sự kiện\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-227\" id=\"menu-item-227\">\n   <a href=\"https://lienquan
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.enchantments (`https://lienquan.garena.vn/hoc-vien/phu-hieu/`)
```json
{
  "title": "Phù Hiệu | Liên Quân Mobile",
  "top_classes": [
    [
      "li.menu-item",
      36
    ],
    [
      "div.st-badges__skill",
      31
    ],
    [
      "div.st-badges__skill--head",
      31
    ],
    [
      "h4.st-badges__skill--title",
      31
    ],
    [
      "article.st-badges__skill--content",
      31
    ],
    [
      "li.menu-item-type-post_type",
      23
    ],
    [
      "li.menu-item-object-page",
      23
    ],
    [
      "li.menu-item-type-custom",
      13
    ],
    [
      "li.menu-item-object-custom",
      13
    ],
    [
      "div.st-badges__item",
      4
    ],
    [
      "h2.st-badges__item--name",
      4
    ],
    [
      "div.st-badges__item--content",
      4
    ],
    [
      "ul.st-badges__item--skills",
      4
    ],
    [
      "a.active",
      4
    ],
    [
      "div.active",
      4
    ]
  ],
  "sample_items": [
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.current-menu-ancestor.current-menu-parent.current_page_parent.current_page_ancestor.menu-item-has-children.menu-item-1710",
      "text_preview": "Gameplay Tướng/Skin Trang Bị Bảng ngọc Phụ Trợ Phù Hiệu Chế độ chơi",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page current-menu-ancestor current-menu-parent current_page_parent current_page_ancestor menu-item-has-children menu-item-1710\" id=\"menu-item-1710\">\n <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-gameplay.png\"/>\n  <span>\n   Gameplay\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1709\" id=\"menu-item-1709\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/tuong-skin/\">\n    Tướng/Skin\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1708\" id=\"menu-item-1708\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/trang-bi/\">\n    Trang Bị\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1704\" id=\"menu-item-1704\">\n   <a href=\"https://lienquan.garena.vn/hoc-vien/bang-ngoc/\">\n    Bảng ngọc\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-1707\" i\n... [TRUNCATED]"
    },
    {
      "selector": "li.menu-item.menu-item-type-post_type.menu-item-object-page.menu-item-has-children.menu-item-4468",
      "text_preview": "Tin tức Cập nhật Sự kiện Mở bán Hợp tác Giải đấu Cẩm nang",
      "html_preview": "<li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-has-children menu-item-4468\" id=\"menu-item-4468\">\n <a href=\"https://lienquan.garena.vn/tin-tuc/\">\n  <img src=\"https://lienquan.garena.vn/wp-content/uploads/2024/07/icon-news.png\"/>\n  <span>\n   Tin tức\n  </span>\n </a>\n <ul class=\"sub-menu\">\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-224\" id=\"menu-item-224\">\n   <a href=\"https://lienquan.garena.vn/cap-nhat/\">\n    Cập nhật\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-228\" id=\"menu-item-228\">\n   <a href=\"https://lienquan.garena.vn/tin-tuc/su-kien/\">\n    Sự kiện\n   </a>\n  </li>\n  <li class=\"menu-item menu-item-type-post_type menu-item-object-page menu-item-227\" id=\"menu-item-227\">\n   <a href=\"https://lienqu
... [TRUNCATED]
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 3.updates (`https://lienquan.garena.vn/cap-nhat/`)
```json
{
  "sample_articles": [
    {
      "title": "Cập nhật ĐIỀU CHỈNH GIỮA MÙA PB VẾT NỨT THỜI KHÔNG – 17.11.2026 Xin chào các Kiện Tướng, Liên Quân Mobile sẽ tiến hành cập nhật không gián đ",
      "url": "https://lienquan.garena.vn/dieu-chinh-giua-mua-pb-vet-nut-thoi-khong-17-11-2026/",
      "parent_class": "p-news__posts--list"
    },
    {
      "title": "Cập nhật ĐIỀU CHỈNH GIỮA MÙA PB VẾT NỨT THỜI KHÔNG – 30.10.2026 Xin chào các Kiện Tướng, Liên Quân Mobile sẽ tiến hành cập nhật không gián đ",
      "url": "https://lienquan.garena.vn/dieu-chinh-giua-mua-pb-vet-nut-thoi-khong-30-10-2026/",
      "parent_class": "p-news__posts--list"
    },
    {
      "title": "Cập nhật THÔNG BÁO CẬP NHẬT HIỂN THỊ GIÁ NẠP QUÂN HUY QUA GOOGLE PLAY Xin chào các Kiện Tướng, Hội đồng xin thông báo: giao diện nạp Quân Hu",
      "url": "https://lienquan.garena.vn/thong-bao-cap-nhat-hien-thi-gia-nap-quan-huy-qua-google-play/",
      "parent_class": "p-news__posts--list"
    },
    {
      "title": "Cập nhật ĐIỀU CHỈNH GIỮA MÙA PB VẾT NỨT THỜI KHÔNG – 15.10.2026 Xin chào các Kiện Tướng, Liên Quân Mobile sẽ tiến hành cập nhật không gián đ",
      "url": "https://lienquan.garena.vn/dieu-chinh-giua-mua-pb-vet-nut-thoi-khong-15-10-2026/",
      "parent_class": "p-news__posts--list"
    },
    {
      "title": "Cập nhật Sự kiện CẬP NHẬT LỖI GIỚI HẠN ĐỔI TRANG PHỤC CỬA HÀNG THỜI GIAN CẬP NHẬT LỖI GIỚI HẠN ĐỔI TRANG PHỤC CỬA HÀNG THỜI GIAN Hội đồng Li",
      "url": "https://lienquan.garena.vn/cap-nhat-loi-gioi-han-doi-trang-phuc-cua-hang-thoi-gian/",
      "parent_class": "p-news__posts--list"
    }
  ],
  "pagination_links": [
    {
      "text": "",
      "href": "https://lienquan.garena.vn"
    },
    {
      "text": "",
      "href": "https://ngame1137.onelink.me/jFUN/OfficialWebsite"
    },
    {
      "text": "",
      "href": "https://lienquan.garena.vn#"
    },
    {
      "text": "Trang chủ",
      "href": "https://lienquan.garena.vn/"
    },
    {
      "text": "Gameplay",
      "href": "https://lienquan.garena.vn/hoc-vien/tuong-skin/"
    },
    {
      "text": "Tướng/Skin",
      "href": "https://lienquan.garena.vn/hoc-vien/tuong-skin/"
    },
    {
      "text": "Trang Bị",
      "href": "https://lienquan.garena.vn/hoc-vien/trang-bi/"
    },
    {
      "text": "Bảng ngọc",
      "href": "https://lienquan.garena.vn/hoc-vien/bang-ngoc/"
    },
    {
      "text": "Phụ Trợ",
      "href": "https://lienquan.garena.vn/hoc-vien/phu-tro/"
    },
    {
      "text": "Phù Hiệu",
      "href": "https://lienquan.garena.vn/hoc-vien/phu-hieu/"
    }
  ],
  "top_classes": [
    [
      "li.menu-item",
      36
    ],
    [
      "li.menu-item-type-post_type",
      24
    ],
    [
      "li.menu-item-object-page",
      24
    ],
    [
      "li.menu-item-type-custom",
      12
    ],
    [
      "li.menu-item-object-custom",
      12
    ],
    [
      "a.p-news__post",
      5
    ],
    [
      "div.p-news__post--img",
      5
    ],
    [
      "div.p-news__post--main",
      5
    ],
    [
      "div.p-news__post--cats",
      5
    ],
    [
      "h2.p-news__post--title",
      5
    ],
    [
      "p.p-news__post--desc",
      5
    ],
    [
      "div.p-news__post--date",
      5
    ],
    [
      "a.page-numbers",
      4
    ],
    [
      "li.menu-item-has-children",
      3
    ],
    [
      "ul.sub-menu",
      3
    ]
  ]
}
```
**Script / AJAX Hints:**
```json
{
  "site_scripts": [
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery.min.js?ver=3.7.1",
    "https://lienquan.garena.vn/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/owl.carousel.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/bootstrap.min.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/fancybox.umd.js?ver=14%3A01-08.10.2026",
    "https://lienquan.garena.vn/wp-content/themes/aov-2024/assets/js/script.js?ver=14%3A01-08.10.2026"
  ],
  "ajax_or_api_hints": [
    "https://lienquan.garena.vn/wp-admin/admin-ajax.php"
  ],
  "inline_json_vars": [
    "aov"
  ]
}
```

## 4. Sample Patch Article (`https://lienquan.garena.vn/dieu-chinh-giua-mua-pb-vet-nut-thoi-khong-17-11-2026/`)
```json
{
  "content_container": "article.p-news__single--content.article",
  "tables_count": 5,
  "headings_or_strong": [
    {
      "tag": "strong",
      "text": "MỤC LỤC"
    },
    {
      "tag": "h1",
      "text": "SỰ KIỆN"
    },
    {
      "tag": "h2",
      "text": "Lối vào sự kiện: Sảnh – Trung tâm sự kiện – Đại Chiến Ghép Thú"
    },
    {
      "tag": "h2",
      "text": "Làm lại chiêu thức Butterfly! Chơi Butterfly nhận thưởng!"
    },
    {
      "tag": "h2",
      "text": "Bình chọn trang phục, tham gia sự kiện nhận thưởng"
    },
    {
      "tag": "h1",
      "text": "CÂN BẰNG TƯỚNG"
    },
    {
      "tag": "h2",
      "text": "Butterfly"
    },
    {
      "tag": "strong",
      "text": "Chiêu 1:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 2:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 3:"
    },
    {
      "tag": "h2",
      "text": "Arduin"
    },
    {
      "tag": "strong",
      "text": "Nội tại:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 2:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 3:"
    },
    {
      "tag": "h2",
      "text": "Grakk"
    },
    {
      "tag": "strong",
      "text": "Nội tại:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 1"
    },
    {
      "tag": "h2",
      "text": "Dirak"
    },
    {
      "tag": "strong",
      "text": "Chiêu 2: Hồi chiêu: 12.5s (-0.5s/cấp chiêu) → 10s (-0.4s/cấp chiêu)"
    },
    {
      "tag": "h2",
      "text": "Richter"
    },
    {
      "tag": "strong",
      "text": "Chiêu 1:"
    },
    {
      "tag": "strong",
      "text": "Chiêu 3:"
    },
    {
      "tag": "h2",
      "text": "Fennik"
    },
    {
      "tag": "strong",
      "text": "Chiêu 1:"
    },
    {
      "tag": "h2",
      "text": "Dyadia"
    }
  ],
  "balance_change_line_samples": [
    "Chỉnh cụ thể:",
    "Chiêu 2: Gỡ bỏ hiệu ứng: Sau khi trúng đích không còn tăng tỷ lệ chí mạng nữa. ST mục tiêu đầu tiên: 100(+20/cấp chiêu)(+0.3 Công vật lý) STVL → 50(+10/cấp chiêu)(+0.15 Công vật lý) STP, chắc chắn chí mạng. Nhận ba đòn đánh thường cường hóa gây ST thêm: 20(+4/cấp chiêu)(+0.3 Công vật lý) ST Phép, chắc chắn chí mạng.",
    "ST mục tiêu đầu tiên: 100(+20/cấp chiêu)(+0.3 Công vật lý) STVL → 50(+10/cấp chiêu)(+0.15 Công vật lý) STP, chắc chắn chí mạng.",
    "Chiêu 3: Hiệu ứng hồi máu: hồi khi dấu ấn kết thúc hoặc mục tiêu bị hạ → hồi phục khi mỗi lần gây ST lên mục tiêu bị đánh dấu. Tỷ lệ hồi máu: 35% → Gây lên tướng hồi 20%, gây lên mục tiêu 
... [TRUNCATED]
```
