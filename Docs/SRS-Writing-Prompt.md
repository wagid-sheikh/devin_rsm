Act as the best and senior Most business analyst. Your job is to create a full fledged SRS that can be given to chatGPT to write/generate FULL code in ONE GO. ChatGPT to produce 2 Zip files. Zip File1: Backend and Zip File: Frontend

SRS to be developed for Mobile First Web based Retail Store billing system.

Backend: FastAPI (all REST APIs to be 100% async) + Python + PostgreSQL

Frontend: React (Vite)

Basic Tables/Modules that I can think of:

1. Backend APIs to be 100% async and backend APIs to consider the need of frontend
2. Frontend calling Backend APIs to be in sync with code developed/written so that there's no mismatch
3. Rate limiting, throttling to be handled well in advnace in the code itself.
4. Cost Center -  a unique value master. Cost center to be replicated to companies and their stores, should have it's own master table
5. Tenant/Company Master (having multiple stores and each having it's own address, GST#)
6. Company Stores (some stores would be under franchise agreement and some independent. Stores will have weekly and monthly sales, delivery & collection targets)
7. Users
8. Roles
9. User & Roles Mapping
10. User with Store Access
11. Customer Master (Customer has one or more contact person & their contact number and also has one or more address for pickup & delivery)
12. Items Master
13. Items Rate (Rates will be classified base company rate, and then customer specific rate)
14. Customer Packages (maintaing packge signup date, value, package usage again bills/services and package balance. Once customer will signup for one or more package)
15. Customer Orders - tied to a store [one or more orders can be exported to PDF]
16. Customer order details [Each order item can be classifed as service type, quantity (units, kg)]
17. Orders Tags (one for each article of the order)
18. Order to Invoice [One of more invoice can be exported to PDF]
19. Invoice Details
20. Invoice payments [one or more invoice paymetns can be exported to excel, csv, PDF]
21. Order Pickup & Drop Tracking with rider distance
22. Expenses Tracking/Management
    1. Company Expenses - facility to attache bill and/or payment screenshots. Expenses to be classfied as recurring or otherwise
    2. Store Expenses- generally petty cash expenses
23. Stores staff management
    1. Daily Attendance, cut-off time, automated half-day marking, absent marking (overrides can be perfomed by Area Manager, Store Manager or Company Owner)
    2. Weekly Off (once per week but never on Fri,Sat & Sun)
    3. Leaves application & approval
    4. Reimbursements application & approvals and merging to payroll
    5. Payroll management
24. Centralised Document Management
    1. Enables storage of all documents
       1. Like bills of all expenses
       2. GST certificates
       3. Or any other customer related documents
       4. Or any other documents
       5. User/Employee documents like PAN, Driver License, Resume, Address Proof, AADHAR,
25. WhatApp
    1. Feedback Module to send feebdback message to each customer upon delivery of their orders
    2. Promotional campaign
26. Bank Reconciliation
27. Franchise Stores Sales Report merging into this system
28. Income, Sales, Expenses daily, weekly, monthly yearly report
29. Comprehensive Analytics Dashboard for
    1. Company Owner
    2. Area Manager (having one or more stores under him/her)
    3. Store Manager
30. B2B Leads Management
31. B2B orders tracking & management
32. B2B billing (can use above tables/modules but categorisation/demarcation needed)
33. Browser based application, security management, token handling etc.
34. Test Driven Development
35. Backend Deployable independently - it's own git repo and uses docker
36. Front Deployable Independently - it's own git repo and uses docker
37. Database Version control management
38. Secrets to be not stored in .env files and to be passed using githb workflow secrets
39. Local Development to not use docker (Local Development uses MacBook)
40. Details and guidance of local development setup, DEV deployment & PROD deployment to be provided (DEV & PROD deployment users ubuntu)
41. Include directory trees as chatgpt tends to hallucinate when working on longer assignment.
42. Also add checklist that chatgpt signs off after completion of each task and sub-tasks so that chatgpt remains on track and delivers
43. You are supposed to produce a comprehensive SRS in markdown file that I can download later. First produce output on screen and then upon confirmation provide a downloadable markdown file.
44. Code generated/written should implement all standard industry practices and totally modular

Anything else I missed, please ask so that can we can include it.
