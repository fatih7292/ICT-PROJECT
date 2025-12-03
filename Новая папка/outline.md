# Feedback System - Project Outline

## File Structure

```
/mnt/okcomputer/output/
├── index.html              # Main landing page with search
├── professor.html          # Professor profile page
├── add-review.html         # Add review form page
├── main.js                 # Main JavaScript functionality
├── resources/              # Images and assets folder
│   ├── hero-bg.jpg         # Hero background image
│   ├── professor-1.jpg     # Professor profile images
│   ├── professor-2.jpg
│   ├── professor-3.jpg
│   ├── professor-4.jpg
│   ├── professor-5.jpg
│   ├── professor-6.jpg
│   ├── university-bg.jpg   # University campus images
│   └── student-avatars/    # Student avatar images
│       ├── avatar-1.jpg
│       ├── avatar-2.jpg
│       └── ...
```

## Page Breakdown

### 1. index.html - Main Landing Page
**Purpose**: Primary entry point with search functionality and featured content

**Sections**:
- Navigation bar with logo and menu
- Hero section with search bar and animated background
- Featured professors carousel
- Top-rated professors grid
- Search results display area
- Footer with university partners

**Key Features**:
- Real-time search with autocomplete
- Filter by subject, university, rating
- Sort options and pagination
- Popular professors showcase

### 2. professor.html - Professor Profile Page
**Purpose**: Detailed view of individual professor with reviews and ratings

**Sections**:
- Professor header with photo and basic info
- Rating overview with visual breakdown
- Reviews timeline with filtering options
- Add review button and form
- Related professors suggestions

**Key Features**:
- Interactive rating display
- Review filtering and sorting
- Helpful/not helpful voting
- Review submission form

### 3. add-review.html - Add Review Page
**Purpose**: Dedicated page for submitting detailed professor reviews

**Sections**:
- Progress indicator for form steps
- Professor identification (pre-filled)
- Rating selection interface
- Review text area with guidelines
- Course and semester selection
- Anonymity options
- Preview and submit

**Key Features**:
- Multi-step form with validation
- Character counters and guidelines
- Preview functionality
- Draft saving

## Interactive Components

### Search System
- **Location**: Main page header
- **Functionality**: Real-time search with filters
- **Data**: Mock database of 50+ professors

### Rating Interface
- **Location**: Professor pages and review forms
- **Functionality**: 5-star rating with hover effects
- **Visual**: Animated stars with physics

### Review Cards
- **Location**: Professor profile pages
- **Functionality**: Expandable, votable, reportable
- **Features**: Timestamp, helpful count, course info

### Professor Cards
- **Location**: Search results and featured sections
- **Functionality**: Quick preview with ratings
- **Interaction**: Click to view full profile

## Data Structure

### Professor Data
```javascript
{
  id: "prof_001",
  name: "Dr. Sarah Johnson",
  subject: "Computer Science",
  university: "Stanford University",
  image: "professor-1.jpg",
  rating: 4.8,
  reviewCount: 127,
  specialties: ["AI", "Machine Learning"],
  courses: ["CS101", "CS201"],
  bio: "Leading researcher in artificial intelligence..."
}
```

### Review Data
```javascript
{
  id: "review_001",
  professorId: "prof_001",
  author: "Student123",
  rating: 5,
  date: "2024-01-15",
  course: "CS101",
  semester: "Fall 2023",
  text: "Excellent professor with clear explanations...",
  helpful: 23,
  anonymous: true
}
```

## Technical Implementation

### Libraries Used
1. **Anime.js** - Smooth animations and transitions
2. **ECharts.js** - Rating distribution charts
3. **Splide.js** - Professor carousels
4. **p5.js** - Particle background effects
5. **Matter.js** - Physics-based rating interactions
6. **Pixi.js** - Advanced visual effects
7. **Shader-park** - Dynamic background gradients

### JavaScript Modules
- **Search Module**: Real-time filtering and autocomplete
- **Rating Module**: Interactive star ratings and charts
- **Review Module**: Form handling and validation
- **Animation Module**: Page transitions and micro-interactions
- **Data Module**: Mock data management and storage

## Content Requirements

### Images Needed
- 6 professor profile photos (diverse, professional)
- 12+ student avatar images
- Hero background (university/academic theme)
- University campus images
- Subject/category icons

### Text Content
- Professor biographies and specialties
- Sample reviews (50+ realistic entries)
- University descriptions
- Subject category descriptions
- Help text and guidelines

## Responsive Design

### Breakpoints
- Mobile: 320px - 768px
- Tablet: 769px - 1024px
- Desktop: 1025px+

### Mobile Optimizations
- Touch-friendly rating interface
- Collapsible search filters
- Swipe navigation for reviews
- Optimized form layouts