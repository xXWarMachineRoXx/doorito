# Doorito
> A 2024 hobby door access management project with Face recognition and auto push attendance to Kredily or potentially any HRMS software

Doorito is a simple Door access management (Face Indentification/Recognition + Fingerprint ) + Time/Breaks Tracking software integration layer ( upcoming )
It can work with Zkteco devices and it has a simple to use interface built with streamlit that can be extended. 

# Motivation
- Core Motif:  We had this requirement at work to track breaks and also auto push attendance to Kredily from the Identix Biometic Device automatically ( which doesn't even have wifi 🥲)
- Side Motif: I had this project thing assigned to me before but I couldn't do it as I didn't know about dll functions and how to use them
- Side Side motif :  I didn't wanna log in my attendance manually and continously forgot to logout. It didn't seem natural and I think just walking in/out the door should be counted as your attendance ( hence the name doorito :D ) 

# Getting Started

1. Switch to the other doorito/lucifer branch as the main branch only contains a copy of the dlls needed for the software to work.
2. After cloning the branch, run `pip install -r requirements.txt` (make sure you have streamlit installed) and then run `streamlit run app.py`.
3. VOila! Register your face and name and also change the config file to make sure you have a redis account ( make a free one / [while its free 🥺](https://redis.io/blog/what-redis-license-change-means-for-our-managed-service-providers/))
4. Right now it only tracks how long were you looking at the screen, but future attemps will change that to detect what time did you leave and come back.


# Future Work 
1. Breaks Management
2. Hardware Sizing
3. Better UI
4. Cleaner Code.



# How to contribute ✌️

1. Follow #Getting Started
2. Put up a PR.
3. I'll merge it and voila, you just made this software a lot better for a lot of people who might use it 🥳. ( especially people like me who spent more than a week trying to get Timetrack lite to work with Identix/Zkteco biometric device.)
