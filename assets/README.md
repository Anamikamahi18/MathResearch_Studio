# Assets Directory

This directory stores static assets for MathResearch Studio.

## Contents

```
assets/
├── images/           # Application screenshots for README and GitHub Release
│   ├── upload_page.png
│   ├── library_page.png
│   ├── search_page.png
│   ├── assistant_page.png
│   ├── graph_page.png
│   ├── notation_page.png
│   ├── statistics_page.png
│   └── export_page.png
│
├── demo/             # Demo video files or links
│   └── demo_video_link.md
│
└── logo/             # Project logo and branding (future)
```

## Populating This Directory

After your **screenshot session** (see [`docs/demo_assets.md`](../docs/demo_assets.md)):

1. Capture screenshots of all 8 application pages
2. Save them here as `images/<page_name>.png`
3. Update `README.md` to embed them:
   ```markdown
   ![Upload Page](assets/images/upload_page.png)
   ```
4. Upload them to the GitHub Release as additional assets

## Demo Video

After recording (see [`docs/demo_recording_checklist.md`](../docs/demo_recording_checklist.md)):

1. Upload the video to YouTube or Loom
2. Create `assets/demo/demo_video_link.md` with the URL
3. Add the link to `README.md` and the GitHub Release body

---

*MathResearch Studio v1.0.0 · Assets Directory*
