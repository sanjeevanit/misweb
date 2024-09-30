# MIS - Management Information System for Technical College Gampaha

## Project Overview
MIS (Management Information System) is a web application developed to streamline the management process for both staff and students at a technical college. The system integrates various functionalities such as student and staff attendance using face recognition and allows students to pay their course fees through Stripe transactions. The project was developed using Django as the web framework and MySQL as the database system.

## Features
- **Attendance System**: Uses face recognition to manage and track attendance for staff and students.
- **Payment System**: Integrated Stripe API for secure course fee transactions.
- **User Management**: Supports multiple user roles, including students and staff, with appropriate permissions and access levels.
- **Dashboard**: A comprehensive dashboard for both students and staff to access information like attendance records, payment history, and more.
- **Notifications**: Sends notifications and updates to users about course updates and payments.

## Tech Stack
- **Backend**: Django 4.2.2
- **Frontend**: HTML, CSS, JavaScript (with Django templates)
- **Database**: MySQL
- **Face Recognition**: `face-recognition` library
- **Payment Gateway**: Stripe API
- **IDE**: PyCharm

## Installation

### Prerequisites
Ensure that you have the following installed:
- Python 3.x
- Django
- MySQL database
- Stripe API keys

### Libraries and Dependencies
Install the required libraries using pip:

```bash
pip install -r requirements.txt
