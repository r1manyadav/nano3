# 📸 Image Upload Feature - User Guide

## Quick Start: How to Add Images to Questions

### For Teachers 👨‍🏫

#### Step 1: Create/Edit Question
```
Teacher Dashboard → Create New Test → Add Question
```

#### Step 2: Add Image *(New!)*
```
┌─────────────────────────────────────┐
│ Question ${number}                  │
├─────────────────────────────────────┤
│ Question Text:                      │
│ [Enter question here...]            │
│                                     │
│ 📷 Question Image (Optional):       │ ← NEW FEATURE
│ [Choose File] [No file selected]    │
│ Supported: JPG, PNG, GIF, WebP      │
│ Max 5MB                             │
│                                     │
│ [Image Preview Shows Here]          │ ← Live Preview
├─────────────────────────────────────┤
│ Select Options...                   │
│ ○ Option A                          │
│ ○ Option B                          │
│ ○ Option C                          │
│ ○ Option D                          │
│ [✓ Mark Correct Answer]             │
└─────────────────────────────────────┘
```

#### Step 3: Submit
- Test is created with or without images
- Images are stored in database automatically
- Students can immediately take the test

---

### For Students 👨‍🎓

#### Step 1: Take Test
```
Login → Student Home → Available Tests → Select Test
```

#### Step 2: View Question with Image *(New!)*
```
┌─────────────────────────────────────────┐
│ Question 3 of 10          [Progress]    │
├─────────────────────────────────────────┤
│                                         │
│ "Identify the shape in this image:"     │
│                                         │
│ ┌───────────────────────────────────┐   │
│ │                                   │   │
│ │      [IMAGE APPEARS HERE]         │   │
│ │      Just like any web image      │   │
│ │      Max height: 400px            │   │
│ │      Responsive sizing            │   │
│ │                                   │   │
│ └───────────────────────────────────┘   │
│                                         │
│ Select your answer:                     │
│ ○ A. Circle                             │
│ ○ B. Square      ← Correct Answer       │
│ ○ C. Triangle                           │
│ ○ D. Rectangle                          │
│                                         │
│ [ ✓ Save & Next ] [ ⊘ Skip ]           │
│ [ ⭐ Mark Review ] [ 📋 Review Only ]   │
└─────────────────────────────────────────┘
```

#### Step 3: Answer & Continue
- Images display automatically
- Works with new 4-button answer system
- No change to test-taking process

---

## 🎨 Image Format Support

| Format | Supported | Notes |
|--------|-----------|-------|
| JPG / JPEG | ✅ | Compressed, best for photos |
| PNG | ✅ | Lossless, best for diagrams |
| GIF | ✅ | Animated or static |
| WebP | ✅ | Modern, smaller file size |
| **OTHERS** | ❌ | SVG, BMP, TIFF not supported |

---

## 📊 Recommended Image Sizes

| Use Case | Size | Format | Tips |
|----------|------|--------|------|
| **Graphs** | 400×300px | PNG | Clear, simple |
| **Diagrams** | 500×350px | PNG | High contrast |
| **Photos** | 600×400px | JPG | Natural colors |
| **Maps** | 500×400px | PNG | Labels visible |
| **Charts** | 450×300px | PNG | Data clear |
| **Equations** | 300×200px | PNG | Good resolution |

**Maximum allowed: 5MB per image**

---

## ✨ Feature Capabilities

### What Images Can Do:
✅ Support any visual question  
✅ Display during entire test  
✅ Work in test submissions  
✅ Show in result reviews  
✅ All browsers/devices  
✅ No external links needed  

### Technical Benefits:
✅ Images embedded in database  
✅ No separate file server  
✅ Single database backup includes images  
✅ Portable between computers  
✅ Fast loading (no HTTP requests)  

---

## 🔒 Security & Limitations

### Safety Features:
- File type validation (image only)
- File size limit (5MB)
- No code execution possible
- Images stored as inert data

### Limitations:
- Images cannot be animated (except GIF)
- SVG not supported
- Maximum 5MB per image
- No image editor built-in
- Teachers must own/have rights to images

---

## 📋 Common Use Cases

### 1️⃣ Geometry Problems
```
Question: "What is the area of this triangle?"
Image: [Triangle diagram with measurements]
Options: 
- A. 30 cm²
- B. 45 cm² (correct)
- C. 60 cm²
- D. 90 cm²
```

### 2️⃣ Science Diagrams
```
Question: "Label the parts of the cell"
Image: [Labeled cell diagram]
Options:
- A. Mitochondria
- B. Nucleus (correct)
- C. Ribosome
- D. Golgi Body
```

### 3️⃣ Language Learning
```
Question: "What object is shown?"
Image: [Picture of apple]
Options:
- A. Manzana (correct in Spanish)
- B. Naranja
- C. Plátano
- D. Pera
```

### 4️⃣ Map Questions
```
Question: "What is the capital of this country?"
Image: [Map of France]
Options:
- A. Paris (correct)
- B. Lyon
- C. Marseille
- D. Nice
```

### 5️⃣ Graph Analysis
```
Question: "What trend does this graph show?"
Image: [Line graph showing growth]
Options:
- A. Steady growth (correct)
- B. Decline
- C. Fluctuation
- D. No change
```

---

## 💡 Tips for Best Results

### For Teachers:

1. **Keep images clear** - Use good contrast, readable fonts
2. **Consistent sizing** - All question images similar height
3. **Test first** - View question as student before publishing
4. **Avoid spoilers** - Don't include answer hints in image
5. **File format** - PNG best for diagrams, JPG for photos
6. **Compress images** - Use online tools if over 5MB
7. **Label clearly** - Use text labels and annotations

### For Students:

1. **Check images** - Read entire image, not just obvious part
2. **View clearly** - Zoom in if image seems unclear
3. **Read caption** - Question text often provides context
4. **Reference carefully** - Look at specific details in image
5. **Note scale** - Some images include scale/dimension info

---

## 🔍 Troubleshooting

### Image Not Showing in Teacher Dashboard Preview?
```
✓ Check file size (< 5MB)
✓ Check file format (JPG, PNG, GIF, WebP only)
✓ Wait a moment for preview to load
✓ Try different browser
✓ Clear browser cache
```

### Image Not Displaying to Students?
```
✓ Ensure test was saved successfully
✓ Check image displays in test preview
✓ Try refreshing page
✓ Check browser console for errors
✓ Ensure image was selected when creating question
```

### Image File Won't Upload?
```
✓ Check file size - must be under 5MB
✓ Check file format - must be JPG, PNG, GIF, or WebP
✓ Try saving image in different format
✓ Compress image using online tools
✓ Check file name (avoid special characters)
```

---

## 📱 Device Compatibility

### Desktop
- ✅ Windows (Chrome, Firefox, Edge, Safari)
- ✅ Mac (Chrome, Firefox, Safari)
- ✅ Linux (Chrome, Firefox)

### Mobile  
- ✅ iOS (Safari, Chrome)
- ✅ Android (Chrome, Firefox)

**Images are responsive** - automatically scale to fit screen

---

## 🎯 Image Quality Checklist

Before uploading an image:

- [x] Image is relevant to question
- [x] Image is clear and readable
- [x] File size is under 5MB
- [x] File format is supported (JPG/PNG/GIF/WebP)
- [x] Image is teacher-owned or licensed
- [x] Image contrast is good
- [x] Image dimensions reasonable (not too wide/tall)
- [x] Image properly labeled/annotated
- [x] No answer hints visible in image
- [x] Image displays correctly in preview

---

## ? Frequently Asked Questions

### Q: Can I edit image after creating question?
**A:** Not directly. You can delete question and recreate with new image, or update test to add/remove images.

### Q: Do images work with markers and reviews?
**A:** Yes! Images display same way whether marked for review or unattempted.

### Q: Can students annotate images?
**A:** Not currently. Teachers must provide annotated images.

### Q: Do images count toward database size limit?
**A:** Yes. ~1KB per image in base64 format. 100 images ≈ 100KB added.

### Q: Can I use online image URLs?
**A:** No. Must upload actual image files. They're converted to base64.

### Q: What happens to images if I delete test?
**A:** Images are deleted with the test (no storage waste).

### Q: Can students download images?
**A:** Yes, using right-click → Save image (browser default).

---

## 📞 Support

**Image Upload Feature v1.0** - Ready to use!

For issues or questions:
1. Check troubleshooting section above
2. Review common use case examples
3. Verify image file requirements
4. Test with different image format

---

**Happy teaching with images! 📸✨**
