# 🍋 Little Lemon - Restaurant Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-REST%20Framework-red)](https://www.django-rest-framework.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)](https://www.mysql.com/)

## 📖 Project Overview

**Little Lemon** is a full-stack restaurant management and ordering platform. This project serves as my final capstone for the **Meta Backend Professional Certificate**.

While the curriculum focused on the backend, I integrated a fully functional, modern frontend to bring the API to life. The frontend was built using the assistance of Large Language Models (LLMs) to accelerate the UI development, allowing me to focus deeply on architecting robust API endpoints, complex database relationships, and seamless authentication.

> **Note:** This open-source release marks the foundational start of this project. While the core functionality is solid, I view it as a strong base for continuous iteration. There is plenty of room for optimization, unit testing, and feature expansion. Contributions and feedback are highly welcome!

---

## ✨ Features

### Core Functionality
- 🔐 **User Authentication**: Secure registration, login, and logout handled via **Djoser** and **Django REST Framework**.
- 📋 **Dynamic Menu**: Interactive menu with category filtering (Starters, Mains, Desserts, etc.).
- 🛒 **Shopping Cart**: Add/remove items, adjust quantities, and review selections before checkout.
- 📦 **Order History**: Detailed user dashboard to review past purchases, date/time stamps, and receipts.

### 🚀 Bonus Additions (Beyond Meta Curriculum)
- 📊 **Admin Dashboard**: A clean analytical dashboard displaying Total Orders, Total Revenue, Items Sold, and Unique Users alongside detailed, granular order logs.
- 📦 **Inventory Management**: An admin panel to add new dishes while tracking real-time stock levels. The UI dynamically alerts staff to low stock (e.g., `Low stock: 2`).
- 🌗 **UX Polish**: Integrated Dark/Light mode toggle for enhanced user experience.

---

## 📸 Screenshots

*(Images are stored in the `/screenshots` folder of this repository)*

| Home Page | Menu Exploration |
| :---: | :---: |
| <img src="screenshots/home.png" width="400"/> | <img src="screenshots/menu.png" width="400"/> |

| Order History | Basket / Checkout |
| :---: | :---: |
| <img src="screenshots/orders.png" width="400"/> | <img src="screenshots/basket.png" width="400"/> |

| Admin: Add Dish | Admin: Dashboard |
| :---: | :---: |
| <img src="screenshots/add_dish.png" width="400"/> | <img src="screenshots/dashboard.png" width="400"/> |

---

## 🛠️ Tech Stack

- **Backend**: Python, Django, Django REST Framework (DRF), Djoser
- **Database**: MySQL
- **Frontend**: Custom HTML/CSS/JS (Accelerated via LLMs)
- **Version Control**: Git

---

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher installed
- MySQL Server installed and running
- Git installed

---

## 🚀 Installation & Setup

Follow these steps to get the development environment running.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/little-lemon.git
cd little-lemon
