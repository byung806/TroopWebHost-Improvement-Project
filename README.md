# TroopWebHost Improvement Project

## Summary
This software project creates a streamlined email system and better manage troop data in TroopWebHost (TWH: `troopwebhost.org`), a platform that allows each Boy Scout Troop leader to manage their troop’s adult training and events. Each Boy Scout troop leader has to update the trainings for Boy Scouts volunteers (adults) manually, and our project improves the convenience and efficiency of the process of managing adults in the troop.

Actively used to manage Troop 1094 Darnestown (100+ scouts/adults).

## Features
![twh](https://github.com/user-attachments/assets/17bf3785-2293-40ab-ab79-e8add54d66f5)
(real troop members redacted for privacy)

- Email template system
- Scraping from TroopWebHost website
- Email sending system
- Member selection system
- Member training sort functionality

## How does it work?

The application is built using Python and Tkinter.

The UI library is Forest (https://github.com/rdbende/Forest-ttk-theme).

Scraping is done using the `requests` library. HTML parsing is done with `bs4` (BeautifulSoup), and troop scouts and adults are processed into rows.

The chart is a custom implementation that supports member sorting, as well as multi-selection. Email templates are stored in `templates.json`.

The application is also fully threaded with UI/scraping/loading so it stays responsive.

## How to use

Clone the project, and build with pyinstaller.

## License

This project uses MIT license. Check details in `LICENSE`.
