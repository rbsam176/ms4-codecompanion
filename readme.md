# MS4: Code Companion

Full Stack Frameworks with Django Project Submission

## Access

View the deployed project: [here](https://codecompanionapp.herokuapp.com)

View the Github repo: [here](https://github.com/rbsam176/ms4-codecompanion)


## Example Service input

If you want to test adding a new Service to Code Companion, feel free to use the values below:

**FontAwesome icon class**: fas fa-hand-pointer

**Name**: Portfolio Review

**Endpoint**: portfolio-review

**Description**: Get feedback and advice on your portfolio before applying for positions

**Price**: 40

**Price type:** per session (1 hour)

**Duration:** 1

**Bullet point 1:** Refine your portfolio using the advice of a senior Companion to shape your first impression with potential employers.

**Bullet point 2:** Work on how to effectively communicate your development journey and discuss the challenges your faced along the way.



## Table of Contents
* [Strategy](#Strategy)
	* [User Stories & Project Objectives](#user-stories--project-objectives)
* [Scope](#scope)
	* [Current Features](#current-features)
	* [Long-term Vision](#long-term-vision)
* [Code Walkthrough & Challenges](#code-walkthrough--challenges)
	
	* [Auto-suggest](#auto-suggest)
	* [Storing Images in MongoDB](#storing-images-in-mongodb)
	  * [Version 1 (Image URL)](#version-1-image-url)
	  * [Version 2 (FileStack API)](#version-2-filestack-api)
	  * [Version 3 (Base64 in MongoDB)](#version-3-base64-in-mongodb)
	  * [Version 4 (ImageKit.io API)](#version-4-imagekitio-api)
	* [Dynamic Queries](#dynamic-queries)
	* [Word cloud (tasting notes)](#word-cloud-tasting-notes)
	* [Pagination](#pagination)
	* [Checkbox toggles](#checkbox-toggles)
	* [Filter criteria validation](#filter-criteria-validation)
	* [View Structure](#view-structure)
	* [Database Schema](#database-schema)
	
* [UX](#ux)
  * [Wireframes ](#wireframes)
  * [Visual Structure/Language](#visual-structurelanguage)
  * [Colour](#colour)
  * [Typography/Icons](#typographyicons)

* [Testing](#testing)

  * [Accessibility](#accessibility)
  * [Performance, Best Practices, SEO](#performance-best-practices-seo)

  * [Manual testing](#manual-testing)
  * [Code Validation](#code-validation)
* [Deployment](#deployment)
* [Credits & Attributes](#credits--attributes)

## Strategy

### User Stories & Project Objectives

*"As a user..."*

<details>  
<summary>I want to get almost immediate support for a coding problem without having to wait long for a response</summary>
Code Companion allows you to book sessions with experienced developers who can help you through resolving issues with your code. Sessions are available to begin every 30 minutes depending on the availabilty of our companions.
</details><br>

<details>  
<summary>I want to be able to learn from an experienced developer face to face, rather than through message board or StackOverflow responses.</summary>
Every session is available face to face using Jitsi, a web conferencing platform. Screen sharing is supported so you can have the Companion walk you through your issue while you're scrolling through your code.
</details><br>

<details>  
<summary>I want to be able to have a one-off sessions on preparing for employment without having to do a full coding bootcamp.</summary>
Every session is purchased individually without the need to bulk-buy or subscribe. You can purchase a session on Interview Preparation, or a Code Review if you find yourself at the stage where you're ready to apply for positions.
</details><br>

## Scope

## Current Features

### CRUD

- #### Create

  - Visitors to Code Companion can signup and create an account.
  - Users can select a service, date, Companion, and time to purchase. 
  - Users ask new questions to be added to the FAQ.
  - Users can convert their account to be a Companion profile, allowing them to take sessions and earn money.
  - Users can add notes to their order for the Companion to see
  - Companions can set which days of the week they are available.
  - Companions can set what services they are able to offer.
  - Superusers/Admin users can add a new Service
  - Superusers/Admin users can review questions submitted by users to the FAQ and choose to approve or delete
  - Superusers/Admin users can add new questions to the FAQ

- #### Read

  - Users can view all services and sort them by most popular (based on number of orders) or price low>high / high/low
  - Users can see their order history from their profile
  - Users can see their upcoming sessions from their profile
  - Users on the homepage can see the top 4 most read FAQ entries based on number of clicks.
  - Users can run a search command and receive search results matching Services or Companions
  - Companions can see their upcoming sessions they need to teach from their profile
  - Companions can see notes written by users for upcoming sessions
  - Superusers/Admin users can see questions submitted by users pending approval

- #### Update

  - All users can change their email-address and password from their profile
  - First name and Last name must be entered to convert account to be a Companion profile
  - Companions can update their availability or sessions offered from their profile
  - Companions can convert their profile back to being a regular user
  - Superusers/Admin users can edit questions submitted by users for approval and respond with answers
  - Superusers/Admin users can edit existing services
  - Superusers/Admin users can edit existing FAQ entries

- #### Delete

  - Superusers/Admin users can delete existing FAQ entries
  - Superusers/Admin users can delete user submitted FAQ entries pending approval
  - Superusers/Admin users can delete services

### Features

- #### Base template

  - Dropdown menu showing all Services and a link to Compare Services so they can all be seen on one page.
  - Collapsible search menu on desktop
  - Basket button with live counter of number of sessions in bag
  - Responsive footer which changes structure depending on breakpoint. Easy access to links to various Services and FAQ questions.

- #### Homepage

  - The hero container changes its content depending on whether user is logged in or not. Default view is a hero banner inviting users to sign up for an account. Entering the email will take the user to the Sign Up page with their typed-in email already populated. The logged-in view provides a button that links the user to their profile page where they can quickly view upcoming orders.
  - 
  - Lineup of companies that Companions have experience working for, to give users an impression of the backgrounds and experience that can be shared if they sign up for a session.
  - Testimonials from previous students, to offer perspectives to further entice prospective students.
  - Lineup of web technologies that our Companions have experience using. This offers some background on what sort of support can be offered before the user visits the Services page.
  - FAQ preview. This displays 4 frequently asked questions, and the 4 shown are dynamic depending on how many times users have viewed the question on the main FAQ page.
  - Links to every Service offered, plus an additional link to the Compare Services page so the user can see them all on one page.
  - If the user is not logged in, an additional section is at the bottom of the homepage that allows them to enter their email and it be transferred to the Sign Up page with the email already populated.


- #### Services

  - **Service detail**<br>
	The user selects the date within the next 5 working days (Mon-Fri), the Companion they wish to work with and the time. These values are populated dynamically. On page load it will check if there is a Companion available on each day, and it will disable any day that has no Companiosn. Once the date has been selected it will check which Companions are scheduled that day and populate the dropdown accordingly. Selecting a Companion will then populate the times between 9am-6pm. If the user has selected the same day they're viewing then it will remove any elapsed time slots. Any time slots where the Companion is already in a session will be disabled. If all time slots have elapsed, or if all time slots are disabled then a message is displayed informing the user to select a different date. If the user is not logged in then the Add To Bag button is not displayed and a link to login is. If the user is logged in but hasn't selected a time yet, the Add To Bag button will be disabled.	

  - **Compare Services**<br>
	- All services are displayed in a grid view that is responsive depending on breakpoint.
	- User is able to sort by Most Popular (based on number of orders), or Price Low>High / High>Low
	- Sign up email input is shown to users who aren't logged in

  - **Sorting:**

    - Date (Most Recent) [default]
    - Date (Oldest)
    - Name (A > Z)
    - Name (Z > A)
    - Brand (A > Z)
    - Brand (Z > A)

  - **Pagination**<br>allows the results to be split over multiple pages. CoffeeDB will only present 6 submissions per page as this occupies a reasonable amount of screen space on all devices from mobile to desktop without introducing a huge area for the user to have to scroll through. Displaying only 6 results per page also reduces the amount of time needed to load a page, and reduces the amount of data downloaded if the user didn't want to search through all results. The user is also informed about how many results were returned from their filter criteria, along with the page that they are on and how many pages their criteria is split across.<br>[Click here to read about how the pagination code was written](#pagination).

  - **Validation**<br>When a user makes a filter selection, they are presented with the filters listed above the results so that if they wish to remove one of the filters they are able to. This also validates their selection so they know if they've made a mistake.<br>[Click here to read about how this validation code was written](#filter-criteria-validation).

  - **Navigation**<br>As the homepage has an immediate hero container presenting the CoffeeDB logo and a dedicated navigation, a secondary nav was needed for when the user scrolled down past this container. The mobile nav appears when the user begins to scroll and its positioning becomes 'sticky' when the secondary nav hits the top of the users viewport. If the navigation is collapsed and the user scrolls back to the top, the navigation is closed automatically.

- #### Submission card

  - The top left corner displays the average rating for each submission, allowing the users to see the consensus of the quality of the coffee immediately from the browse page.<br>If the submission being viewed was submitted by the user viewing it, then the top right corner displays an EDIT button which takes the user through to the editing page. The user-submitted image is displayed prominently and along with the brand and coffee name, which are linked to the View Submission page if clicked.
  - Attributes are then shown, which include roast type, origin, whether it is organic and an optional link to the coffee roasters website.
  - A maximum of 4 flavour notes are permitted and shown on each submission card, and each one is linked to a filter criteria showing all submissions containing the clicked note.
  - Finally the username of the user who made the submission is shown, so that others can see what other submissions the user has made.

- #### Add

  - Image uploader which will only accept image files and is sent to an external image hosting service.<br>[Click here to read more about how the images are kept in the database](#storing-images-in-mongodb).<br>[Click here to read about how the image hosting API code was written](#version-4-imagekitio-api).
  - Brand and Origin dropdown 'select' inputs. This presents a list of brands/origins that they user can select. The values have some default values, and the other values come from whatever users have previously entered into the database. Another option is to select 'Other...' which will then disable the dropdown selector and dynamically create a text input field below. This allows the user to type in a new brand/origin that doesn't exist as an option already. [Autocomplete](#auto-suggest) has been added to this text input to assist users in case they're entering a value that already exists.
  - Notes only permits the user to 'check' 4 values, the other notes become disabled when 4 have been selected by the user, until one is unchecked. The user can type in a new flavour note if one does not exist as an optional already, [Autocomplete](#auto-suggest) has been added to this text input. If 3 ntoes have been checked and the user types in a 4th manually then the disabled state still gets trigerred.
  - Submitting data to the databse will add any new attributes like custom brand/origin/notes to the options in the filter section on the Browse page. They also become options if any user then goes to add a new entry.
  - For desktop users, a live preview of their input is available on the right half of the screen. This dynamically updates with the users input while they're typing, including the image they have uploaded. This is primary so that the user can see what their submission will look like before they submit. In particular, this provides validaiton that the image they have uploaded is proportioned correctly, so the image live preview is also available for mobile users.

- #### Profile (submissions)

  - This page is publicly accessible by anyone. However if the user logged in is the user viewing the profile page, they also have access to a sub-navigation menu that allows them to go to two additional pages, one to update their account details and another to delete their account.
  - Displayed at the top informs users of the first name of the user, the date they signed up to CoffeeDB and how many submissions they have contributed.
  - Pagination has been included to split their submissions if they exceed 6.
  - Sort options are available.

- #### Profile (update account) / Signup

  - If updating their account, users can make changes to their first name, last name, email and username without having to enter their password. 
  - Whenever signing up or updating an account, entering a first name and last name will automatically fill in the username with the two names concatenated as a suggestion.
  - When updating an account, changing the password requires the user to enter their existing password.
  - Both signing up and updating an account share a UI that validates if the users password meets the criteria. 
  - Sign Up / Change Password submit buttons are disabled by default and become active when the password criteria is met.
  - Updating the username updates the session token.

- #### Profile (delete account)

  - 'Delete my account permanently' is disabled until the user has entered at least 3 characters into both text input fields. 
  - Clicking 'Delete my account permanently' will prompt a second button to appear, labelled 'Permanently Delete' to ensure the user understands the action they're committing to.

- #### View Submission

  - The UI is made up of two sections, the submission card and options to rate or review the submission.
  - If a user attempts to rate a submission when they're not logged in, they are prompted with a link to login.
  - The review text input field is disabled if a user is not logged in.
  - When the user hovers over the rating icons it will fill in the icons up to the one they are hovering over.
  - Submitting a rating will update the 'Your rating' section, the 'Average rating' will reflect the changes in numbers and the submission card average in the top left corner will update.
  - Writing a review will count down the character counter to inform the user of how many characters they have left.
  - If the user has already submitted a review, the review text input field will already contain their review so they can edit it or replace it with another.
  - The character counter will reflect the number of characters if the review already exists and is in the text input field on page load.
  - Reviews will show the review text, username of the reviewer, timestamp of when the review was written and their rating if it exists.
  - The review timestamp is recorded in UTC but displayed to the user in their local timezone.
  - If more than 3 reviews exist, a link to 'View all reviews' is triggered.

- #### All reviews

  - [Click here to see an example](http://ms3-coffeedb.herokuapp.com/view/608408fa9f27253818935e4e) of a submission containing more than 3 reviews which triggers a link to appear to visit an 'All Reviews' page.
  - All reviews for a submission are listed on one page.
  - The ability to sort reviews by date or number of ratings is available.
  - As the 'all reviews' page is 2 pages deep, meaning the previous page is not accessible via the navigation menu, a back button is presented which returns the user to the 'View Submission' page.

- #### 404

  - If a user tries to access a page that doesn't fit the correct state, eg. a logged in user trying to access a signup page... then they are redirected to a relevant page, in this example they are redirected to their profile page.
  - If the user tries to access a page where the endpoint does not exist, they are presented with a 404 error page with a link to take them back to the homepage.

- #### Login

  - The user is able to login with their email and password.
  - Their username is used as the session token, which is updated if they ever change their username.
  - A link is provided to signup if the user hasn't an account already.



## Long-term vision

- Currently when inputting a value that cannot be a duplicate, eg. an email, username, coffee name etc. it does not tell you in real time that is already exists, it requires the form to be submitted to then provide validation. In a future build I would introduce AJAX to be able to provide live validation for a better user experience.
- A bug exists where if a user deletes their account their reviews still exist. For GDPR reasons it would be better to remove these, but it will also impact the user experience in that the reviews will still link to the users profile which no longer exists since deletion.
- Currently a user is not able to delete ratings or reviews, only edit them. This should be introduced in a future build.
- While CoffeeDB demonstrates usage of a non-relational database, it also makes use of MongoDB's ability to include limited relationships between sets of data. While this is functional in this current build, for CoffeeDB to expand and provide features such as recommending coffee to users based on their previous ratings/reviews, a transition to a dedicated relationship database management system such as MySQL would be beneficial.
- In a future build I would like to include the ability to share profile pages over social media. This would be beneficial to the user as it would provide easy means to share their favourite coffee with friends. It would be beneficial to CoffeeDB in that it would promote word-of-mouth advertising.
- Within the users profile page it should provide recommendations of coffee based on the what ratings the user has given to other coffee submissions. This suggestion would be based submissions that were also highly rated by users that rated the common submission.
- A future implementation should include the ability to have different user types, with different permissions. Currently all users are treated the same, there is no admin user other than who has access to the code itself (me). I would like to introduce an admin user so that reviews/submissions can be removed easily if they contain inappropriate material.
- The current build of CoffeeDB only permits sorting by rating on the 'All reviews' page. All other sort functionality is purely by brand name/coffee name and submission date. This was partly due to the nature of MongoDB not fully supporting relationships. A change to the schema may allow this, by separately ratings and reviews to their own collection, but the benefits need to be weighed when deciding whether to proceed with a document based database such as MongoDB versus a relational database like MySQL.
- Currently a user is unable to easily see all submissions they have rated or reviewed, it would rely on them remembering the submission and finding it via Browse. I would like this to be introduced within their profile page in a future build.
- The ability to 'watch' other users so that you are notified if someone you follow has submitted a new coffee, or recently reviewed/rated a coffee. This would introduce a light social network to CoffeeDB which I believe could influence users to return more often.
- The search container is positioned at the top of the second half of the homepage when viewing on desktop. Due to the grid system in bootstrap it is moved below other containers when viewing on mobile. For consistency I would like to update this to be more consistent.
- A bug exists with the collapsible filter controls on the Browse page that should be rewritten in a future build. If the user clicks to open the filter controls more than once in quick succession it will confuse the toggle state and be in an open state when the controls are closed, and vice-versa. This is more likely a Bootstrap component issue, but a workaround can be found, or alternatively a different method of writing a collapsible container can be included.

# Code Walkthrough & Challenges

## Auto-suggest

In order to provide suggestions to the user while they are typing into a text input field, I have used jQueryUI's autocomplete plugin. I used this plugin in my MS2 project which was written entirely in JavaScript. 

However, because CoffeeDB is a Flask app, the values don't exist natively in the front end, so this presented a challenge on how I was going to pass this information to the source list for autocomplete. If the information was visible on the page, this would be fairly easy, as jQuery could read from this list in the DOM and use this as the source. However, the information that needed to be passed was a list of brands, coffee names and flavour notes.

My research pointed me to the use of AJAX, which I would like to include in a future build as I believe it would be useful elsewhere on CoffeeDB, such as verifying if a users input already exists in real-time (like signing up and typing in a username). My solution was to create a new view called autocomplete which wouldn't be linked to any on CoffeeDB, so it would only be accessible to those who know the URL. While this isn't secure, I determined that this was an appropriate use-case as the data was not sensitive. I considered using this method to include verification of pre-existing usernames, but deemed a list of all usernames to be too sensitive.



```python
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    # GATHER DATA TO BE PASSED TO FRONTEND
    values = {
        "brands": list(getCoffeeData()['brand_names']),
        "names": list(mongo.db.beans.distinct('name')),
        "origins": list(getCoffeeData()['origin_types']),
        "notes": list(getCoffeeData()['unique_notes'])
    }
    # CONVERT LIST TO JSON
    json_values = json.dumps(values)
    # SEND TO TEMPLATE
    return jsonify(autocomplete_values=json_values)
```

I created the view, fed the corresponding data into a new dictionary named 'values' and had this converted to JSON and be returned. 



```javascript
    // AUTOCOMPLETE ASSIGNMENT
    $.getJSON('/autocomplete', function(data) {     
        // PARSES JSON DATA PULLED FROM MONGODB
        var jsonParsed = JSON.parse(data.autocomplete_values);
        // CONCATENATES BRANDS AND NAMES TO SINGLE LIST
        var autocompleteData = jsonParsed.brands.concat(jsonParsed.names)
        // ASSIGNS LIST OF BRANDS, NAMES TO SEARCH INPUT AUTOCOMPLETE
        $( "#searchInput" ).autocomplete({
            source: autocompleteData
        });
    });
```

In the JavaScript code of any page that needs the auto-suggest feature I had a function communicate with the JSON data and then pass it to jQueryUI's autocomplete source.



## Storing Images in MongoDB

This was probably the most time-consuming challenge I faced while working on CoffeeDB. 

### Version 1 (Image URL)

The original implementation of allowing users to input an image with their coffee submission was simply to allow them to enter a url to the image into a text input field. This would then store the url as the value to a key within the submission document in the 'beans' collection in MongoDB. This worked, but it didn't produce a great experience on mobile, as copying and pasting the url feels long-winded. It also didn't have a way of verifying for sure that url entered resulted in an image. I briefly implemented some validation that checked the url ended with a filetype such as .jpg, .png etc. but increasingly more websites are obscuring their url from including the filetype.

### Version 2 (FileStack API)

I had decided that I wanted a file picker. This would solve the issue for mobile users having to copy/paste in order to input an image, as they could directly upload from their photo album (after saving an image from a website) or directly take a photo of the coffee themselves. As MongoDB can't directly store images, I decided to research into implementing a third party API that meant the file picker was actually sending the users image file to an external service which provided the hosting. FileStack worked great, and had the added benefit of presenting the user with a sleek UI that allowed them to crop/resize their image before submitting. My implementation of FileStack's API was done on the frontend, in JavaScript, so this presented a challenge of how to pass the returned image URL to Flask. I decided to allow users the choice between using this file picker or entering an image url. This meant I could use JavaScript to return the uploaded image's URL into the text input field, which would then get submitted along with the rest of the submission data in the POST request. Unfortunately, it became apparent that FileStack's free tier was very limiting as I soon ran out of my free allowance for number of requests to their server and the file picker stopped functioning when the user tried clicking on it.

### Version 3 (Base64 in MongoDB)

While working on MS2 I had worked with base64 to encode some CSV data to allow the user to download it to their disk. I decided to encode the users uploaded image in base64 and store this string in MongoDB. This was the solution that I had landed on for the longest time as it seemed to tick all the boxes and work without any issues. 

Unfortunately all of a sudden CoffeeDB's homepage, browse page and profile pages all became extremely slow to use. After some troubleshooting I discovered this was because of MongoDB, as when I tried to view the data in the database it was also very slow to use. After contacting MongoDB's developer support they explained that because I was using the free tier they had throttled my account as it had sent 12gb of requests within the period of a week. 

I initially didn't understand how this was possible as the combined size of data in MongoDB came to just a few megabytes. I looked through my code and discovered that where I was not able to write a MongoDB find query to get access to sub-arrays (ratings), I had written a loop to extract the information I needed and this meant iterating over the large base64 strings over multiple times. I was able to mitigate this by using 'projection' in my MongoDB query.



```python
    # # COLLECTION CONTAINING ALL DOCUMENTS WITH RATINGS
    ratingsTrue = mongo.db.beans.find({"rating": {"$exists": True}},
                    projection={"rating": 1, "brand": 1, "name": 1})
```

Using 'projection' meant I could ask it to only return the values I needed. While this would have definitely improved the size of the requests I was making, it was too late and the throttling had been enabled and I was advised it would be a while until it would be disabled. I decided to avoid storing base64 encoded images in MongoDB and explore another API solution.

### Version 4 (ImageKit.io API)

The final solution I settled on was similar to version 2, in that I implemented a third party API to store the images externally. Similarly, the direct image url would be stored in MongoDB. I was able to find a service that offered a generous 20gb of storage for free and provided a Python API, which resolved the issue of how to pass the url from the front-end to the back.



```python
def uploadImage(image):
    imagekitUpload = imagekit.upload_file(
        file = image,
        file_name = image.filename,
        options={
            "is_private_file": False,
        },
    )
    return imagekitUpload
```

I created the above function, guided by the ImageKit documentation, and had it return the response JSON. I have another function named 'gatherInputs' which is used twice on CoffeeDB, on both the Add page and Edit page. This gathers all of the user inputs of a coffee submission, and calls the uploadImage function in order to get the image url to store into MongoDB.



## Dynamic Queries

The default view of the Browse page is to show all results, in order of most recently added. The user is able to select from multiple options to form their criteria, this includes roast type, searchable brand name/coffee name, origin, whether submissions should be organic, and tasting notes. In order to process the query, the form sends a GET request which is processed by the browse view in Python. 

I created an empty list called 'dynamicQuery' which gets added to depending on the arguments of the GET request. If arguments are detected for each input in the filter controls then it gets appended to 'dynamicQuery'. Once all of the arguments have been appended, a MongoDB find query is made using '$and' so that multiple arguments can be passed.

There are two instances where the query doesn't use '$and'. The search input field where the user can type in the brand name or coffee name uses '$or' so that it can check whether the query text matches either the 'brand' key or 'name' key.

The other instance is when the user can choose between the results displaying **all** or their selected tasting notes, or **any** of the selected notes. This uses MongoDB's '$all' and '$in' respectively.



**<i>Shortened</i> example of the dynamicQuery appending the arguments for 'roast' and 'notes':**

```python
dynamicQuery = []

if request.args.getlist("roast"):
            dynamicQuery["$and"].append({"roast": {"$in":
                                        request.args.getlist("roast")}})
if request.args.getlist('tag'):
            if request.args['conditionType'] == "all":
                dynamicQuery["$and"].append({"notes": {"$all":
                                            request.args.getlist('tag')}})
            if request.args['conditionType'] == "any":
                dynamicQuery["$and"].append({"notes": {"$in":
                                            request.args.getlist('tag')}})
beans = mongo.db.beans.find(dynamicQuery)
```



## Word cloud (tasting notes)

One of the most fun challenges to work on was forming a '[word cloud](https://en.wikipedia.org/wiki/Tag_cloud)' to represent which tasting notes were most common in the database. I intentionally didn't research how to go about writing this, as I wanted to challenge myself to see if I could do it independently. 

The word cloud function receives 2 arguments, a list and a unique list. For my usage, I passed a list of all tasting notes used in the database, duplicates included, and another list containing only the unique values (using MongoDB's 'distinct' query).

```python
# CREATES TUPLE WITH UNIQUE ITEM AND ITS NUMBER OF OCCURANCES
    itemCount = []
    for x in uniqueList:
        itemCount.append((x, list.count(x)))
    itemCount = sorted(itemCount, key=lambda item: item[1], reverse=True)
```

I used a for loop to iterate over the unique list and count how many times that particular note occurred in the non-unique list. This list was then sorted in order of the most frequently occurring note in the database.



```python
    itemPercentage = {}
    for item in itemCount:
        # RETURNS NUMBER OF NOTES
        length = len(uniqueList)
        # RETURNS HOW MANY TIMES NOTES OCCUR
        occurance = item[1]
        # DIVIDES TOTAL NUMBER OF NOTES BY OCCURANCE
        percentage = occurance / length * 100
        # ADDS TO DICTIONARY
        itemPercentage[item] = percentage
```

Rather than having the fixed number of how many times each tasting note occurred, I wanted the value to be a percentage relative to the length of the list of unique values. 



Having the percentage allowed me to then organise the font size of the note depending on what bracket it fell into. I decided on 4 font sizes, determined by whether the note fell into <25%, >25%, >50% or >75%. The filter criteria only shows 10 notes by default, the list passed to the view is in order of the highest percentage, so I applied a CSS class called 'extra-note' to any values after 10 which had 'display: none' applied to it. This display property gets reversed by JavaScript if the user clicks the button to see all notes.



## Pagination

Along with the word cloud, creating my own pagination was also a very exciting challenge. Similarly, I didn't include [flask-paginate](https://pythonhosted.org/Flask-paginate/), a common pagination plugin for Flask apps, I also avoided researching into the functionality in order to pose a challenge to myself. 

As the pagination is used in multiple places throughout CoffeeDB, I wrote the UI code in its own Jinja Macro so it could be easily imported. To write the logic, I wrote a function that received 2 arguments, the number of items to be viewed on any given page and the total amount of items to be displayed.

The default 'page' variable value is 1, offset is set to 0 and the 'pageQuantity' variable, which represents how many pages the data will be split over, is calculated by dividing the total number of items by the number of items per pay (6 in CoffeeDB's usage).

Within the function it checks for GET request arguments, specifically looking for a page number which the UI sends any time the user clicks on the next page or previous page buttons, the value is calculated by taking the current page number and adding or subtracting 1.

Once the function receives the page number via the GET request, it multiplies this number (subtracting 1 to represent the page number the use came from, not landed on) and multiplies it by the argument passed to it representing how many items to be shown on each page (6). This all results in an 'offset' variable which can be passed to the find query given to MongoDB when making the ['dynamicQuery' (see above)](#dynamic-queries) request.



```python
# CREATES OFFSET AMOUNT BASED ON SPECIFIED QUANTITY SHOWN PER PAGE
def pagination(perPage, dataCount):
    page = 1
    offset = 0
    pageQuantity = math.ceil(dataCount / perPage)
    if 'page' in request.args:
        page = int(request.args.get("page"))
        currentPage = page - 1
        offset = currentPage * perPage
    return offset, perPage, page, dataCount, pageQuantity
```

Pagination function, also returning values that are passed to the view that form 'Showing results 1 to 6 (Page 1 of 4)' for example.



```python
# REASSIGNS VALUES TO PAGINATION VARIABLES
offset, perPage, page, beansCount, pageQuantity = pagination(
  					6, mongo.db.beans.count_documents(dynamicQuery))
# REASSIGNS BEANS VARIABLE TO INCLUDE QUERY
# AND PAGINATION OFFSET/LIMIT
beans = mongo.db.beans.find(
  dynamicQuery).sort("_id", -1).skip(offset).limit(perPage)
```

Demonstrating sending the offset and limit queries to MongoDB.



## Checkbox toggles

Throughout CoffeeDB you will see custom toggle buttons, they are used for specifying criteria to the Browse filter, along with adding a submission. These toggles are actually masked checkboxes which have their default checkbox UI hidden using CSS. The button text is still wrapped in a label, making these custom toggles accessibility-friendly.



## Filter criteria validation

When a user makes a filter criteria query, they are presented with some UI validation which allows them to remove individual elements of their query, while informing them of the actions they just made.

<img src="static/assets/filter-validation.png" alt="Filter criteria validation screenshot" style="zoom:50%;" />



This validation is entirely built using Jinja. Jinja requests the current URL arguments, checks for origin, roast, organic status and tasting notes and for each category it forms a new GET request without including the element that was clicked. This results in the page being refreshed without the element the user wanted to remove from the criteria. 

In addition to this, if the user opened the filter validation panel again they would find the options they had checked already highlighted, and if an origin or tasting note was ordinarily hidden in the 'show more' section, they would find that it is not grouped in the hidden section and instead if highlighted and visible immediately.



## View structure

This diagram describes how the Jinja macros fit into the project and which views are inheriting which base templates.

<img src="static/assets/basemacro.png" alt="Diagram of base templates and macros" style="zoom:50%;" />



# Database Schema

<img src="static/assets/schema.png" alt="Screenshot of MongoDB schema" style="zoom:50%;" />



# UX

## Wireframes

<img src="static/assets/wireframe.png" alt="Wireframe"/>

The project started with making a wireframe of the homepage and Browse page. You can see that the UI evolved fairly substantially, but from the beginning the UI decisions led the functional implementations, demonstrated by the early wireframe showing a word cloud as a way to display tasting notes. The dropdown selector within the search input field was eventually dropped in favour of a universal search, so it searches for brands and coffee names without the user having to specifically select which one.



## Visual structure/language

The structure throughout CoffeeDB is made up of *cards*, making use of a Bootstrap UI class. This provided a clean, evenly spaced vertical structure to house the information about the coffee, which could be repeated in a loop easily (eg. Browse), or used individually (eg. homepage). 

The homepage presents a hero splash page, with the CoffeeDB logo occupying the majority of the viewport, along with a dedicated navigation bar. This almost mimics the UX of an app launching, rather than being immediately met with your typical website structure you are instead presented with the brand and have easy access to the pages the user is likely wanting to visit first, eg. Browse or Add.

Further down on the homepage are a series of containers that relay the state of the database in that moment the user is visiting. It shows the most recent addition, the top 5 highest average ratings and the most recent 3 reviews. These all link the user to 'view submission' pages, providing an alternative way to discover coffee than just entering filters on the Browse page.

In order to keep the UX consistent, and to make use of repeatable code, both the Add/Edit pages are virtually the same, with small differences such as the title and form parameters, and the Signup/Update Account pages again relying on very similar code to produce a familiar experience.

By default, the Browse page filter controls are hidden, so the user is immediately greeted with the most recent coffee submissions so their discovery can begin. Bootstrap's collapse class was used in order to produce a smooth scrolling animation. 



<img src="static/assets/old-checkboxes.png" alt="Original tasting notes screenshot" style="zoom:50%;" />

An older version of the checkbox UI before redesigning them to have a hidden checkbox.



<img src="static/assets/logos.png" alt="Logo iterations" style="zoom:50%;" />

A selection of logos made before deciding on what became the final logo.



## Colour

Given that CoffeeDB is largely about coffee, it made sense to have the colours match accordingly. However from the beginning I wanted to avoid using too much brown as I felt it created quite a dark theme and didn't feel fresh or inviting. I settled for a orangey/brown hue, with slight variations of the same colour throughout.

Main theme colour: #F8A825

Secondary theme colour: #643F00



<img src="static/assets/strongborders.png" alt="Screenshot showing thick border" width="200"/><img src="static/assets/boxshadow.png" alt="Screenshot showing box-shadow" width="300" />



A reoccurring motif throughout CoffeeDB is the use of strong borders and/or box-shadows. I felt as though having strong borders made identifying certain elements of the structure very quick and easy. A users first impression when they arrive at a page and they immediately know where to look as it is boxed in specific areas. Adding the box-shadow to certain elements, but not all, provided 'depth' to the design so it didn't feel overly boxy and square.



## Typography/Icons

All non-default fonts were imported via Google Fonts.



<img src="static/assets/logo.png" alt="Final logo" style="zoom:50%;" />

The CoffeeDB logo, found on the homepage and the navigation bar is made up of two fonts. 'Coffee' is using Pacifico, and 'DB' is using Codystar. 



<img src="static/assets/coffeeheader.png" alt="Header font screenshot" style="zoom:50%;" />

Headers, such as the title of a coffee submission, are using a bold Montserrat.



*All other fonts are using default Bootstrap sans-serif fonts.*

------

<img src="static/assets/bean.png" alt="Homepage bean icon" style="zoom:50%;" />

3 bean icons are scattered on the homepage, providing a visual cue that the theme of the website is coffee. [Source of icon](https://pngtree.com/freepng/coffee-beans-icon-outline-style_5104840.html).



<img src="static/assets/404.png" alt="Logo iterations" title="Logo iterations" style="zoom:40%;" />

A variation on the bean icon presented on the 404 error page of an unknown endpoint, edited by me from source above.



<img src="static/assets/arrow.png" alt="404 bean icon" style="zoom:50%;" />

Arrow icons throughout CoffeeDB all originate from Bootstrap's icons collection.



## Testing

### Accessibility

Whereas an image is displaying, the appropriate alt tags are included. In addition to this, where there is a button element an aria-label has been written to ensure screen readers can identify the nature of the button and what its action is.

**Google Lighthouse's accessibility checker provided the following results:**

| Page                  | Score |
| --------------------- | ----- |
| Homepage              | 95    |
| Browse                | 97    |
| View Submission       | 96    |
| Add/Edit              | 97    |
| Signup/Update Account | 95    |
| Delete Account        | 97    |



### Performance, Best Practices, SEO

After adjusting the MongoDB queries to project only what keys they need [click here for more detail](#version-3-base64-in-mongodb)), performance scores using Google's Lighthouse were greatly improved.

**Google Lighthouse's performance checker provided the following results:**

| Page                  | Performance | Best Practices* | SEO  |
| --------------------- | ----------- | --------------- | ---- |
| Homepage              | 100         | 80              | 90   |
| Browse                | 99          | 80              | 90   |
| View Submission       | 99          | 80              | 90   |
| Add/Edit              | 98          | 80              | 90   |
| Signup/Update Account | 100         | 93              | 100  |
| Delete Account        | 100         | 93              | 100  |

The 'Best Practices' score was only hampered by the fact that the website does not use HTTPS, however this is due to it being deployed using Heroku. If CoffeeDB had a public release it would be hosted elsewhere and use HTTPS to conform to modern security standards.



### Manual testing

As there are numerous pages, and many features to test, I have written a dedicated markdown document detailing the manual test cases to ensure CoffeeDB is operating as expected. 

[Click here to view the manual test cases.](bugtests.md)



### Code Validation

I have tested every page of CoffeeDB using W3's HTML and CSS validator, and all have passed with the exception of anything relating to the fact that the HTML code uses Jinja and anything referencing Bootstrap's own CSS files.

I have run the Python code through a [pep8 compliancy checker](http://pep8online.com), and it has passed without any issues.



# Deployment

CoffeeDB is running off of Heroku, with synchronisation enabled to GitHub. The env.py file, which is not sent externally, contains the necessary MongoDB information (IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME), as well as the public, private and endpoint for the ImageKit API. Before the final deployment I performed a pip freeze in order to update my requirements.txt file with any modules needed to run the app. Since the beginning of developing CoffeeDB I used Git for version control and worked in a virtual environment in order to keep track of which modules were imported, it also has the added benefit of freezing the version of the modules so that if I ever installed a newer version on my computer in the future it wouldn't risk breaking old code reliant on an older version of the module. The final action before releasing CoffeeDB to the public was to set Debug to False within the Python Flask code.



# Credits & Attributes

[Real Favicon Generator](https://realfavicongenerator.net/): for easy image resizing for various favicons.

Animated down arrow on homepage is based on a combination of StackOverflow posts. [Link 1](https://stackoverflow.com/a/32465265) and [Link 2](https://forum.jquery.com/topic/problem-with-using-variable-as-animate-s-properties).

The homepage features two videos in a loop. Both videos are free for non-commercial use, and request a credit to the author. [Link 1](https://www.pexels.com/video/food-wood-dawn-love-7487666/) and [Link 2](https://www.pexels.com/video/food-wood-dawn-man-7487681/).

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/49619445/how-to-append-to-a-list-in-jinja2-for-ansible#comment103228666_49642227) for guidance on how to avoid Jinja printing None when appending to an array.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/10732690/offsetting-an-html-anchor-to-adjust-for-fixed-header) for guidance on how to offset the position of a hyperlink scrolling to an anchor point to account for the height of a stickied navbar.

[ImageKit API Documentation](https://docs.imagekit.io/api-reference/upload-file-api/server-side-file-upload)

[This article](https://philipwalton.github.io/solved-by-flexbox/demos/sticky-footer/) for guidance on how to keep the footer stickied to the bottom of the viewport even if the content fits all on one page.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/11961952/objectid-object-has-no-attribute-gettimestamp/11962000) for guidance on how to extract the timestamp from the Object ID in MongoDB.

The homepage and 404 page both make [use of this icon](https://pngtree.com/freepng/coffee-beans-icon-outline-style_5104840.html), which is free for non-commercial use.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/14091636/get-dict-key-by-max-value/14091645#14091645) for guidance on how to get the top value from a dictionary.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/65823199/dynamic-mongo-query-with-python) which served as inspiration for how I would write a dynamic query for the Browse page.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/55447599/how-to-send-data-in-flask-to-another-page) which helped when trying to figure out how to get the search input value from the homepage to a GET request landing on the Browse page.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/17649875/why-does-random-shuffle-return-none) to help implement a random ordered list.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib) for guidance on how to convert UTC to the users local timezone.

[This page](https://docs.python.org/3/howto/sorting.html) in Python's documentation was used for guidance on how to sort a dictionary by a sub-level value.

Credit to [this Stackoverflow post](https://stackoverflow.com/a/40280312) for answers on how to work around DOM bubbling when targeting a dynamically created element.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/12660124/javascript-jquery-preview-image-before-upload) for guidance on how to convert a user uploaded image to base64 for the purposes of previewing it before submitting a form request.

[This code](https://www.w3schools.com/howto/howto_css_smooth_scroll.asp#section2) from W3 was used to enable smooth scrolling on multiple browsers including Safari.

Credit to [this Stackoverflow post](https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a) on Regex examples for password criteria.

