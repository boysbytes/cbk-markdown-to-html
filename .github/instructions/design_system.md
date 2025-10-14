---
description: 'Framework-agnostic design system and coding standards for building accessible, performant, and maintainable applications'
---

## Core principles

You are assisting with building applications that prioritise **accessibility, performance, maintainability, and exceptional user experience**. Follow these standards rigorously, regardless of framework choice.

## Colour scheme and design system

### Primary colour palette (modern and accessible)

Our colour system follows **WCAG 2.1 Level AA** standards with all colours tested for proper contrast ratios. Text must have a minimum contrast ratio of 4.5:1 with backgrounds, or 3:1 for large text (18pt or 14pt bold).

#### Brand colours

```css
/* Primary - Modern deep blue (professional and trustworthy) */
--color-primary-50: #E8F0FF;
--color-primary-100: #D1E1FF;
--color-primary-200: #A3C3FF;
--color-primary-300: #75A5FF;
--color-primary-400: #4787FF;
--color-primary-500: #1969FF;  /* Main brand colour */
--color-primary-600: #0052E0;
--color-primary-700: #003DB3;
--color-primary-800: #002885;
--color-primary-900: #001357;

/* Secondary - Warm accent (inspired by 2025 trends) */
--color-secondary-50: #FFF5ED;
--color-secondary-100: #FFEBDB;
--color-secondary-200: #FFD7B7;
--color-secondary-300: #FFC393;
--color-secondary-400: #FFAF6F;
--color-secondary-500: #FF9B4B;  /* Warm coral-orange */
--color-secondary-600: #E67A2E;
--color-secondary-700: #B85E23;
--color-secondary-800: #8A4619;
--color-secondary-900: #5C2E0F;

/* Accent - Modern teal (fresh and engaging) */
--color-accent-50: #E6F9F7;
--color-accent-100: #CCF3EF;
--color-accent-200: #99E7DF;
--color-accent-300: #66DBCF;
--color-accent-400: #33CFBF;
--color-accent-500: #00C3AF;  /* Vibrant teal */
--color-accent-600: #00A091;
--color-accent-700: #007D73;
--color-accent-800: #005A55;
--color-accent-900: #003737;
```

#### Neutral colours (high contrast)

```css
/* Neutrals - Carefully calibrated for accessibility */
--color-neutral-50: #FAFAFA;   /* Backgrounds */
--color-neutral-100: #F5F5F5;  /* Light backgrounds */
--color-neutral-200: #E5E5E5;  /* Borders */
--color-neutral-300: #D4D4D4;  /* Dividers */
--color-neutral-400: #A3A3A3;  /* Disabled text */
--color-neutral-500: #737373;  /* Secondary text */
--color-neutral-600: #525252;  /* Body text */
--color-neutral-700: #404040;  /* Headings */
--color-neutral-800: #262626;  /* Dark headings */
--color-neutral-900: #171717;  /* Maximum contrast */
--color-neutral-white: #FFFFFF;
--color-neutral-black: #000000;
```

#### Semantic colours (status and feedback)

```css
/* Success - Green (WCAG AA compliant) */
--color-success-light: #D4F4DD;
--color-success: #059669;      /* 4.5:1 on white */
--color-success-dark: #047857;

/* Warning - Amber (WCAG AA compliant) */
--color-warning-light: #FEF3C7;
--color-warning: #D97706;      /* 4.5:1 on white */
--color-warning-dark: #B45309;

/* Error - Red (WCAG AA compliant) */
--color-error-light: #FEE2E2;
--color-error: #DC2626;        /* 4.5:1 on white */
--color-error-dark: #B91C1C;

/* Info - Blue (WCAG AA compliant) */
--color-info-light: #DBEAFE;
--color-info: #2563EB;         /* 4.5:1 on white */
--color-info-dark: #1E40AF;
```

### Dark mode colours

```css
/* Dark mode palette - Optimised for reduced eye strain */
--color-dark-bg-primary: #0A0A0A;
--color-dark-bg-secondary: #1A1A1A;
--color-dark-bg-tertiary: #2A2A2A;

--color-dark-text-primary: #F5F5F5;    /* High contrast */
--color-dark-text-secondary: #D4D4D4;  /* Medium contrast */
--color-dark-text-tertiary: #A3A3A3;   /* Low contrast */

/* Adjusted brand colours for dark mode (maintain 4.5:1 ratio) */
--color-dark-primary: #5A9AFF;
--color-dark-secondary: #FFB366;
--color-dark-accent: #33CFBF;
```

### Implementation guidelines

#### CSS variables setup

```css
:root {
  /* Light mode (default) */
  --bg-primary: var(--color-neutral-white);
  --bg-secondary: var(--color-neutral-50);
  --text-primary: var(--color-neutral-900);
  --text-secondary: var(--color-neutral-600);
  --border-color: var(--color-neutral-200);
}

[data-theme="dark"] {
  --bg-primary: var(--color-dark-bg-primary);
  --bg-secondary: var(--color-dark-bg-secondary);
  --text-primary: var(--color-dark-text-primary);
  --text-secondary: var(--color-dark-text-secondary);
  --border-color: var(--color-dark-bg-tertiary);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --bg-primary: var(--color-dark-bg-primary);
    --bg-secondary: var(--color-dark-bg-secondary);
    --text-primary: var(--color-dark-text-primary);
    --text-secondary: var(--color-dark-text-secondary);
    --border-color: var(--color-dark-bg-tertiary);
  }
}
```

### Colour usage rules

#### DO ✅

- **Always test colour combinations** with a contrast checker tool
- **Use semantic colour names** (for example, `--color-neutral-900` not `--color-black`)
- **Avoid red-green combinations** as they are difficult for people with colour blindness
- **Provide multiple visual cues** - never rely on colour alone
- **Use colour consistently** across the application
- **Apply primary colour** for main CTAs and interactive elements
- **Use secondary colour** for accents, highlights, and supporting actions
- **Reserve accent colour** for special emphasis and modern flair
- **Test in both light and dark modes** before finalising

#### DON'T ❌

- Never use pure black (#000) on pure white (#FFF) - too harsh
- Do not use low contrast combinations (below 4.5:1 for text)
- Avoid pure red or green for success or error without additional indicators
- Do not use colour as the only way to convey information
- Never use colour combinations that fail WCAG AA standards

### Gradient palettes (modern touch)

```css
/* Modern gradient backgrounds */
--gradient-primary: linear-gradient(135deg, #1969FF 0%, #00C3AF 100%);
--gradient-warm: linear-gradient(135deg, #FF9B4B 0%, #E67A2E 100%);
--gradient-cool: linear-gradient(135deg, #00C3AF 0%, #1969FF 100%);
--gradient-sunset: linear-gradient(135deg, #FF9B4B 0%, #DC2626 100%);

/* Subtle background gradients */
--gradient-light: linear-gradient(180deg, #FFFFFF 0%, #F5F5F5 100%);
--gradient-dark: linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%);
```

### Accessibility testing tools

When implementing colours, use these tools:

- **WebAIM Contrast Checker**: <https://webaim.org/resources/contrastchecker/>
- **Coolors Contrast Checker**: <https://coolors.co/contrast-checker>
- **Adobe Colour Accessibility Tools**: <https://color.adobe.com/create/color-accessibility>
- **Chrome DevTools**: Built-in contrast ratio checker in inspect element

## Component architecture (framework-agnostic principles)

### Component design

- **Keep components small and focused** - each component should have a single responsibility
- **Extract reusable logic** into separate modules or composables
- **Use composition over inheritance** - build complex UIs by composing smaller components
- **Implement proper prop validation** using TypeScript or framework-specific validators
- **Maintain unidirectional data flow** - props down, events up
- **Separate concerns** - keep presentation logic separate from business logic

### File organisation

```plaintext
src/
├── components/        # Reusable UI components
│   ├── Button/
│   │   ├── Button.[ext]
│   │   ├── Button.module.css
│   │   └── index.[ext]
├── composables/      # Reusable logic (Vue/Svelte)
├── hooks/            # Custom hooks (React)
├── stores/           # State management
├── services/         # API calls and external services
├── utils/            # Utility functions
├── styles/           # Global styles, themes, colour variables
│   ├── colors.css    # Colour system definitions
│   └── globals.css   # Global styles
└── assets/           # Images, fonts, static files
```

### Naming conventions

- **Components**: PascalCase (for example, `UserProfile`, `NavigationBar`)
- **Composables or hooks**: camelCase with appropriate prefix (for example, `useAuth`, `useFetch`)
- **Utility functions**: camelCase (for example, `formatDate`, `validateEmail`)
- **Constants**: UPPER_SNAKE_CASE (for example, `API_BASE_URL`, `MAX_RETRY_ATTEMPTS`)
- **Files**: Match component names exactly

## Accessibility standards (WCAG 2.1 Level AA compliance)

### Semantic HTML

- **Always use semantic HTML elements** (`<button>`, `<nav>`, `<main>`, `<article>`, `<header>`, `<footer>`)
- **Never use `<div>` or `<span>` for interactive elements** - use proper semantic elements
- **Use heading hierarchy properly** (h1 → h2 → h3) without skipping levels
- **Use `<form>` elements** for all form controls
- **Use `<label>` elements** associated with form inputs

### ARIA implementation

- **Use ARIA attributes only when semantic HTML is insufficient**
- **Common ARIA patterns**:
  - `aria-label` for elements without visible text
  - `aria-labelledby` to reference existing labels
  - `aria-describedby` for additional context
  - `aria-live` for dynamic content updates
  - `aria-expanded`, `aria-controls` for expandable sections
  - `aria-current` for current page in navigation
  - `aria-hidden="true"` for decorative elements
- **Always include role attributes** for custom interactive widgets

### Keyboard navigation

- **All interactive elements must be keyboard accessible**
- **Ensure logical tab order** (use `tabindex="0"` for custom interactive elements, `-1` to remove from tab order)
- **Support standard keyboard shortcuts**:
  - Enter or Space to activate buttons
  - Arrow keys for navigation in menus or lists
  - Escape to close modals or dropdowns
  - Tab to move forward, Shift+Tab to move backward
- **Implement visible focus indicators** - never remove outline without providing an alternative
- **Trap focus within modals** - prevent focus from escaping modal dialogues

### Colour and contrast

- **Minimum contrast ratio of 4.5:1** for normal text (18px or smaller)
- **Minimum contrast ratio of 3:1** for large text (24px or 19px bold)
- **Never rely on colour alone** to convey information - use text, icons, or patterns
- **Support both light and dark modes** when applicable
- **Use the colour system defined above** - all colours are pre-tested for accessibility

### Forms and inputs

- **Always associate labels with inputs** using `for` attribute (or framework equivalent)
- **Provide clear error messages** with `aria-invalid` and `aria-describedby`
- **Use `autocomplete` attributes** for common fields (name, email, address)
- **Mark required fields** with `aria-required="true"` and visual indicators
- **Group related inputs** using `<fieldset>` and `<legend>`
- **Provide inline validation** with clear feedback

### Images and media

- **Always provide alt text** for meaningful images
- **Use empty `alt=""` for decorative images**
- **Provide captions and transcripts** for audio or video content
- **Include text alternatives** for complex graphics (charts, diagrams)
- **Use responsive images** with appropriate `srcset` and `sizes` attributes

## Responsive design (mobile-first approach)

### Design philosophy

- **Start with mobile layout** (320px minimum) and progressively enhance for larger screens
- **Use relative units** (rem, em, %, vh/vw) instead of fixed pixels
- **Implement fluid typography** using `clamp()` or responsive font sizing
- **Test on real devices** at multiple breakpoints

### Standard breakpoints

```css
/* Mobile-first approach */
/* Base styles: 320px - 767px */

/* Tablet: 768px and up */
@media (min-width: 768px) { }

/* Desktop: 1024px and up */
@media (min-width: 1024px) { }

/* Large desktop: 1440px and up */
@media (min-width: 1440px) { }

/* Extra large desktop: 1920px and up */
@media (min-width: 1920px) { }
```

### Responsive images

```html
<!-- Use srcset and sizes for responsive images -->
<img
  src="image-mobile.jpg"
  srcset="image-mobile.jpg 480w, image-tablet.jpg 768w, image-desktop.jpg 1200w"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  alt="Descriptive alt text"
  loading="lazy"
/>
```

### Touch-friendly design

- **Minimum touch target size: 44x44px** (Apple) or 48x48px (Material Design)
- **Provide adequate spacing** between interactive elements (minimum 8px)
- **Support touch gestures** naturally (swipe, pinch-to-zoom where appropriate)
- **Avoid hover-only interactions** - provide alternatives for touch devices

## Performance optimisation

### General principles

- **Minimise initial bundle size** - lazy load routes and components
- **Optimise images** - use modern formats (WebP, AVIF), appropriate sizes
- **Implement code splitting** - load only what is needed
- **Cache strategically** - use service workers and HTTP caching headers
- **Minimise layout shifts** - reserve space for dynamic content
- **Use resource hints** - `preload`, `prefetch`, `dns-prefetch`

### Loading strategies

- **Critical CSS** - inline above-the-fold styles
- **Defer non-critical JavaScript** - use `defer` or `async` attributes
- **Lazy load images** - use `loading="lazy"` attribute
- **Progressive enhancement** - ensure basic functionality without JavaScript

### State management

- **Keep state as local as possible** - lift state only when necessary
- **Use appropriate state management** - Context API, Vuex, NgRx, or lightweight alternatives
- **Avoid prop drilling** - use composition or state management patterns
- **Normalise complex state** - avoid deeply nested objects

### List rendering

- **Always use unique, stable keys** (not array indices unless list is static)
- **Implement virtualisation** for long lists (virtual-scroller libraries)
- **Paginate or infinite scroll** for large datasets

## User experience (UX) standards

### Loading states

- **Show loading indicators** for async operations over 200ms
- **Use skeleton screens** for better perceived performance
- **Provide progress indicators** for multi-step processes
- **Avoid blocking the UI** - use optimistic updates where appropriate

### Error handling

- **Implement error boundaries** or equivalent for graceful error handling
- **Provide clear, actionable error messages** - avoid technical jargon
- **Offer recovery options** (retry button, alternative actions)
- **Log errors** for debugging (use error tracking services like Sentry)
- **Never expose stack traces** to end users

### Feedback and confirmation

- **Provide immediate visual feedback** for user actions (button states, animations)
- **Show success messages** for completed actions
- **Confirm destructive actions** (delete, permanent changes)
- **Use toast notifications** for non-critical feedback
- **Implement undo functionality** where appropriate

### Navigation

- **Maintain clear navigation hierarchy** - users should always know where they are
- **Provide breadcrumbs** for deep navigation structures
- **Support browser back button** properly in SPAs
- **Implement skip links** for screen reader users to bypass navigation
- **Highlight current page** in navigation menus

## Form handling best practices

### Validation

- **Validate inline** as users complete fields (on blur)
- **Show validation errors clearly** near the relevant field
- **Disable submit button** when form is invalid or submitting
- **Prevent double submissions** by disabling button after first click
- **Validate on both client and server** side

### User input

- **Use appropriate input types** (email, tel, url, number, date)
- **Provide input masks** for formatted data (phone numbers, credit cards)
- **Show character counts** for limited-length fields
- **Save drafts** for long forms when possible
- **Auto-save** periodically for critical forms

### Error messages

```html
<!-- Example: Accessible error message -->
<label for="email-input">Email address</label>
<input
  id="email-input"
  type="email"
  aria-required="true"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" role="alert">
  Please enter a valid email
</span>
```

## Animation and transitions

### Principles

- **Use animations purposefully** - they should enhance UX, not just look decorative
- **Keep animations subtle and fast** (200-400ms typically)
- **Respect `prefers-reduced-motion`** media query

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Common animation uses

- **Page transitions** for smooth navigation
- **Loading animations** to indicate progress
- **Micro-interactions** for button clicks, hovers
- **Revealing content** as it scrolls into view
- **Focus indicators** for keyboard navigation

### Performance considerations

- **Use CSS transforms** (`translate`, `scale`, `rotate`) over position changes
- **Animate `opacity`** instead of `visibility` or `display`
- **Use `will-change`** sparingly and only when needed
- **Avoid animating expensive properties** (width, height, top, left)

## Code quality standards

### Clean code principles

- **Write self-documenting code** with clear variable and function names
- **Keep functions small** - ideally under 20 lines, maximum 50
- **Avoid nested conditionals** - use early returns or guard clauses
- **Comment "why" not "what"** - code should explain what it does
- **Use consistent formatting** - configure Prettier or equivalent

### DRY (don't repeat yourself)

- **Extract repeated logic** into utility functions or composables
- **Create reusable components** for common UI patterns
- **Use constants** for repeated values
- **Avoid copy-paste** - refactor duplicated code

### Error handling

```javascript
// Always handle errors in async operations
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching user:', error);
    // Handle error appropriately (show message, retry, etc.)
    throw error;
  }
}
```

## Security considerations

### Data handling

- **Sanitise user input** before rendering
- **Use framework escaping** - avoid direct HTML insertion
- **Validate data on both client and server** side
- **Use HTTPS** for all API calls
- **Implement Content Security Policy** (CSP) headers

### Authentication

- **Store tokens securely** (httpOnly cookies preferred over localStorage)
- **Implement proper session management**
- **Handle authentication errors gracefully** (redirect to login, show appropriate messages)
- **Use secure password policies** (minimum length, complexity)
- **Implement rate limiting** for login attempts

### Sensitive data

- **Never commit secrets** to version control
- **Use environment variables** for configuration
- **Mask sensitive data** in forms (passwords, credit cards)
- **Implement proper CORS** policies

## Testing standards

### What to test

- **Component rendering** with different props or state
- **User interactions** (clicks, form submissions)
- **Accessibility** (keyboard navigation, ARIA attributes)
- **Error states** and edge cases
- **Integration between components**

### Testing approaches

- **Unit tests** for utility functions and isolated logic
- **Component tests** for UI components
- **Integration tests** for feature workflows
- **End-to-end tests** for critical user journeys
- **Visual regression tests** for UI consistency

### Accessibility testing

- **Use automated tools** (axe-core, Lighthouse)
- **Test keyboard navigation** manually
- **Test with screen readers** (NVDA, JAWS, VoiceOver)
- **Validate HTML** with W3C validator

## Documentation

### Code documentation

- **Document public APIs** with clear descriptions and types
- **Provide usage examples** for complex components
- **Explain non-obvious behaviour** in comments
- **Maintain a component library** (Storybook or equivalent)

### README files

- **Include setup instructions** for new developers
- **Document environment variables** and configuration
- **Provide examples** of common tasks
- **Link to relevant documentation** and resources

## Framework-specific implementations

### React implementation

```javascript
// Custom hook for data fetching
import { useState, useEffect } from 'react';

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}

// Accessible button component
import { forwardRef } from 'react';

const Button = forwardRef(({ variant = 'primary', loading, children, ...props }, ref) => {
  const variants = {
    primary: 'bg-[--color-primary-500] hover:bg-[--color-primary-600] text-white',
    secondary: 'bg-[--color-secondary-500] hover:bg-[--color-secondary-600] text-white',
    accent: 'bg-[--color-accent-500] hover:bg-[--color-accent-600] text-white',
  };

  return (
    <button
      ref={ref}
      className={`px-4 py-2 rounded-lg font-medium transition-colors ${variants[variant]}`}
      disabled={loading}
      aria-busy={loading}
      {...props}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
});
```

### Vue implementation

```javascript
// Composable for data fetching
import { ref, watchEffect } from 'vue';

export function useFetch(url) {
  const data = ref(null);
  const loading = ref(true);
  const error = ref(null);

  watchEffect(async () => {
    try {
      loading.value = true;
      error.value = null;
      const response = await fetch(url.value);
      if (!response.ok) throw new Error('Network response was not ok');
      data.value = await response.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  });

  return { data, loading, error };
}

// Accessible button component
<template>
  <button
    :class="buttonClasses"
    :disabled="loading"
    :aria-busy="loading"
    v-bind="$attrs"
  >
    {{ loading ? 'Loading...' : $slots.default }}
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'accent'].includes(value)
  },
  loading: Boolean
});

const buttonClasses = computed(() => {
  const variants = {
    primary: 'bg-[--color-primary-500] hover:bg-[--color-primary-600] text-white',
    secondary: 'bg-[--color-secondary-500] hover:bg-[--color-secondary-600] text-white',
    accent: 'bg-[--color-accent-500] hover:bg-[--color-accent-600] text-white',
  };
  return `px-4 py-2 rounded-lg font-medium transition-colors ${variants[props.variant]}`;
});
</script>
```

### Svelte implementation

```javascript
// Store for data fetching
import { writable } from 'svelte/store';

export function createFetchStore(url) {
  const { subscribe, set, update } = writable({
    data: null,
    loading: true,
    error: null
  });

  async function fetchData() {
    update(state => ({ ...state, loading: true }));
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      set({ data, loading: false, error: null });
    } catch (error) {
      set({ data: null, loading: false, error: error.message });
    }
  }

  fetchData();

  return { subscribe, refresh: fetchData };
}

// Accessible button component
<script>
  export let variant = 'primary';
  export let loading = false;

  const variants = {
    primary: 'bg-[--color-primary-500] hover:bg-[--color-primary-600] text-white',
    secondary: 'bg-[--color-secondary-500] hover:bg-[--color-secondary-600] text-white',
    accent: 'bg-[--color-accent-500] hover:bg-[--color-accent-600] text-white',
  };
</script>

<button
  class="px-4 py-2 rounded-lg font-medium transition-colors {variants[variant]}"
  disabled={loading}
  aria-busy={loading}
  on:click
  {...$$restProps}
>
  {loading ? 'Loading...' : ''}
  <slot />
</button>
```

### Angular implementation

```typescript
// Service for data fetching
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, map } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class DataService {
  constructor(private http: HttpClient) {}

  fetchData<T>(url: string): Observable<T> {
    return this.http.get<T>(url).pipe(
      map(response => response),
      catchError(error => {
        console.error('Error fetching data:', error);
        throw error;
      })
    );
  }
}

// Accessible button component
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-button',
  template: `
    <button
      [class]="buttonClasses"
      [disabled]="loading"
      [attr.aria-busy]="loading"
    >
      <ng-content *ngIf="!loading"></ng-content>
      <span *ngIf="loading">Loading...</span>
    </button>
  `,
  styles: [`
    button {
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      font-weight: 500;
      transition: background-color 200ms;
    }
  `]
})
export class ButtonComponent {
  @Input() variant: 'primary' | 'secondary' | 'accent' = 'primary';
  @Input() loading = false;

  get buttonClasses(): string {
    const variants = {
      primary: 'bg-primary-500 hover:bg-primary-600 text-white',
      secondary: 'bg-secondary-500 hover:bg-secondary-600 text-white',
      accent: 'bg-accent-500 hover:bg-accent-600 text-white',
    };
    return variants[this.variant];
  }
}
```

### Vanilla JavaScript implementation

```javascript
// Data fetching utility
class DataFetcher {
  constructor() {
    this.cache = new Map();
  }

  async fetch(url, options = {}) {
    const cacheKey = url + JSON.stringify(options);
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      this.cache.set(cacheKey, data);
      return data;
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  }

  clearCache() {
    this.cache.clear();
  }
}

// Accessible button component
class Button {
  constructor(element, options = {}) {
    this.element = element;
    this.options = {
      variant: 'primary',
      loading: false,
      ...options
    };
    this.init();
  }

  init() {
    this.element.classList.add('button', `button--${this.options.variant}`);
    this.updateState();
  }

  setLoading(loading) {
    this.options.loading = loading;
    this.updateState();
  }

  updateState() {
    this.element.disabled = this.options.loading;
    this.element.setAttribute('aria-busy', this.options.loading);
    this.element.textContent = this.options.loading ? 'Loading...' : this.element.dataset.text;
  }
}

// Usage
const button = new Button(document.getElementById('myButton'), {
  variant: 'primary'
});
```

## Styling approaches

### Tailwind CSS (recommended)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#E8F0FF',
          // ...existing code...
          900: '#001357',
        },
        // ...existing code...
      },
    },
  },
  darkMode: 'class', // or 'media'
};
```

### CSS modules

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 200ms;
}

.button--primary {
  background-color: var(--color-primary-500);
  color: white;
}

.button--primary:hover {
  background-color: var(--color-primary-600);
}
```

### Styled components (React)

```javascript
import styled from 'styled-components';

const Button = styled.button`
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 200ms;
  background-color: var(--color-${props => props.variant}-500);
  color: white;

  &:hover {
    background-color: var(--color-${props => props.variant}-600);
  }
`;
```

## When writing code

1. **Always prioritise accessibility** - include ARIA attributes, keyboard support, and semantic HTML
2. **Use the defined colour system** - never use arbitrary colours
3. **Write mobile-first responsive code**
4. **Include error handling** and loading states
5. **Use modern patterns** appropriate to the framework
6. **Add helpful comments** for complex logic
7. **Follow the folder structure** defined above
8. **Implement proper type checking** (TypeScript or PropTypes)
9. **Consider performance** - use memoisation, lazy loading when appropriate
10. **Make it production-ready** - not just a proof of concept
11. **Test colour contrast** - ensure all combinations meet WCAG AA standards
12. **Support dark mode** - implement theme switching when appropriate
13. **Write framework-appropriate code** - use idioms and patterns native to the chosen framework

**Remember: Build applications that are accessible to everyone, performant on all devices, beautiful with our modern colour system, and a joy to use and maintain.**