# Chumbaka Markdown to HTML Converter AI Guide

This document provides instructions for AI coding agents working on the Chumbaka Markdown to HTML converter codebase.

## Project Overview

This is a React-based web application that transforms Markdown text into HTML, specifically formatted for the Chumbaka Learning Management System (LMS). The primary goal is to automate the process of converting educational content into a format compatible with the LMS, including custom styling and structural transformations.

### Key Files

-   `MarkdownToHTMLApp.jsx`: The main React component containing the application's UI, state management, and the core conversion logic. This is the most important file in the project.
-   `index.html`: The entry point for the web application, which includes the necessary HTML structure and styles.
-   `README.md`: Provides a high-level overview of the project and links to related resources.
-   `.github/instructions/`: This directory contains detailed instructions for AI coding agents on various topics, including Markdown content, task implementation, and writing style. When contributing to this project, please adhere to the guidelines in these files.

## Architecture and Core Logic

The application's architecture is centered around the `MarkdownToHTMLApp` component, which manages the user interface and the conversion process. The core logic can be broken down into the following steps:

1.  **Markdown Input**: The user enters Markdown text into a `textarea`.
2.  **State Management**: The component's state, managed with `useState`, tracks the Markdown input and any selected formatting options.
3.  **HTML Conversion**: The `marked` library is used to convert the Markdown to raw HTML.
4.  **Custom Formatting**: The `formatHtml` function applies custom transformations to the raw HTML. This includes:
    -   Converting `<h3>` tags into collapsible `<details>` sections.
    -   Transforming blockquotes with emojis into styled tables.
    -   Adding custom line spacing to improve readability.
5.  **HTML Output**: The formatted HTML is displayed in a read-only `textarea`, ready for copying.

### Custom Formatting Rules

The `formatHtml` function in `MarkdownToHTMLApp.jsx` is responsible for applying project-specific formatting rules. When modifying the conversion logic, it is crucial to understand these rules and their implementation. Pay close attention to the DOM manipulation logic within this function, as it ensures the output meets the requirements of the Chumbaka LMS.

## Development Workflow

The development workflow for this project is straightforward:

1.  **Dependencies**: The project relies on React and the `marked` library for Markdown parsing. Ensure these dependencies are properly installed and managed.
2.  **Running the Application**: The application can be run by opening the `index.html` file in a web browser. For a more robust development environment, consider using a local development server.
3.  **Building the Application**: The project can be built using standard React build tools, such as Create React App or Vite. The build process will generate static files that can be deployed to a web server. The `docs` folder appears to contain a static build of the application.

### Key Commands

While there are no explicit build scripts in the provided files, a typical React project would use the following commands:

-   `npm install`: To install the project dependencies.
-   `npm start`: To start the development server.
-   `npm run build`: To build the application for production.

When working on this project, assume a standard React development environment. If you need to add dependencies, use `npm` or `yarn`.

## Coding Conventions

-   **React Best Practices**: Follow standard React conventions, including the use of functional components and hooks.
-   **Code Style**: Maintain a consistent code style. While no linter configuration is provided, aim for clean, readable code with clear comments where necessary.
-   **DOM Manipulation**: Be cautious when modifying the DOM manipulation logic in the `formatHtml` function. Ensure that any changes are tested thoroughly to avoid breaking the custom formatting rules.
