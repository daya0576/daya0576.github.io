---
layout: post
title: "comp9041 Assignment2 Matelook Implementation"
date: 2016-10-30 00:20:49
comments: true
tags: [comp9041, unsw]
---


> This blog shares my experience of making a simple "Facebook" in two weeks: [http://m.unsw.co/](http://m.unsw.co/)      
And this website is also the second assignment of UNSW COMP9041 assignment2

<!--more-->


> **Technical Details**:    
Flask + cgi     
**The final demo of my website:** [http://m.unsw.co/](http://m.unsw.co/)      
**Github address:** [https://github.com/daya0576/matelook_mini-facebook](https://github.com/daya0576/matelook_mini-facebook)    


> **Gracefully Coding**:    
In this assignment, the most precious thing is not completing all these incredible features, it is doing it `beautifully` and `gracefully`.  
I used **Scrum** to manage each task to improve my efficacy.    
I focused on **readability** and tried my best to make my code pythonic.   
I respect **reusability**, and there is not any repeated code in my project.    
I attach great importance to **performance**: comments, Pagination, etc.     

> ##All the features listed by Andrew       
To assist you tackling the assignments requirements have been broken into several levels in approximate order of difficulty. You do not have to follow this implementation order but unless you are confident I'd recommend following this order. You will receive marks for whatever features you have working or partially working (regardless of subset & order).    
####Display User Information & Posts (Level 0)
The starting-point script you've been given (see below) displays user information in raw form and does not display their image or posts.   
Your web site should display user information in nicely formatted HTML with appropriate accompanying text. It should display the user's image if there is one.    
Private information such e-mail, password, lat, long and courses should not be displayed.    
The user's posts should be displayed in reverse chronological order.    
####Interface (Level 0)
Your web site must generate nicely formatted convenient-to-use web pages including appropriate navigation facilities and instructions for naive users. Although this is not a graphic design exercise you should produce pages with a common and somewhat distinctive look-and-feel. You may find CSS useful for this.    
As part of your personal design you may change the name of the website to something other than matelook but the primary CGI script has to be matelook.cgi.    
####Mate list (Level 1)
When a matelook page is shown a list of the names of that user's mates should be displayed.    
The list should include a thumbnail image of the mate (if they have a profile image).    
Clicking on the image and/or name should take you to that matelook page.    
####Search for Names (Level 1)
Your web site should provide searching for a user whose name containing a specified substring. Search results should include the matching name and a thumbnail image. Clicking on the image and/or name should take you to that matelook page.    
####Logging In & Out (Level 1)
Users should have to login to use matelook.    
Their password should be checked when they attempt to log in.    
Users should also be able to logout.    
####Displaying Posts (Level 2)
When a user logs in they should see their recent posts, any posts from their mates and any posts which contain their zid in the post, comments or replies.    
Comments and replies should be shown appropriately with posts.    
When displaying posts zids should be replaced with a link to the user's matelook page. The link text should be the user's full name.    
####Making Posts(Level 2)
Users should be able to make posts.    
####Searching Posts (Level 2)
It should be possible to search for posts containing particular words.    
####Commenting on Post and replying to Comments (Level 2)
When viewing a post, it should be possible to click on a link and create a comment on that post. When viewing a comment , it should be possible to click on a link and create a reply to that comment.    
####Mate/Unmate Users (Level 3)
A user should be able to add & delete users from their mate list.    
####Pagination of Posts & Search Results (Level 3)
When searching for users or posts and when viewing posts the users be shown the first n (e.g n == 16) results. They should be able then view the next n and the next n and so on.   
####User Account Creation (Level 3)
Your web site should allow users to create accounts with a zid, password and e-mail address. You should of course check that an account for this zid does not exist already. It should be compulsory that a valid e-mail-address is associated with an account but the e-mail address need not be a UNSW address.    
You should confirm e-mail address are valid and owned by the matelook user creating the account by e-mailing them a link necessary to complete account creation.    
I expect (and recommend) most students to use the data format of the data set you've been supplied. If so for a new user you would need create a irectory named with their zid and then add a appropriate user.txt containing their details.    
####Profile Text (Level 3)
A matelook user should be able to add to some text to their details , probably describing their interests, which is displayed with their user details.    
My interests are long walks on the beach and Python programming.    
I plan to use what I've learnt COMP2041 to cure the world of all known diseases.    
It should be possible to use some simple (safe) HTML tags, and only these tags, in this text. The data set you've been given doesn't any include any examples of such text    
You can choose to store this text in the user.txt file or elsewhere,
####Mate Requests (Level 3)
A user, when viewing a matelook page, should be able to send a mate request to the owner of that matelook page. The other user should be notified by an e-mail. The e-mail should containing an appropriate link to the web site which will allow them to accept or reject the mate request.    
####Mate Suggestions (Level 3)
Your web site should be able to provide a list of likely mate suggestions.    
Your web site should display matelook users sorted on how likely the user is to know them. It should display a set (say 10) of matelook users. It should allow the next best-matching set of potential mates or the previous set of potential mates user to be viewed.    
The user should be able to click on a potential mate , see their matelook page (where there will be able to send them a mate request).    
Your matching algorithm should assume that people who have taken the same course in the same session may know each other.    
For example Ralph Firman and Sheryl Crow are both taking 2016 S2 PSYC1011 which should cause your algorithm to make Ralph a more likely mate suggestion for Sheryl (and vice-versa).    
Your matching algorithm should also assume that people may know mates of their mates.    
You may choose to have your matching algorithm use other part of user details.    
Note there are many choices in this matching algorithm so your results will differ from other students. Be prepared to explain how & why your matching algorithm works during your assignment demo. You may chose to have a development mode available which when turned on displays extra information regarding the matching.    
####Password Recovery (Level 3)
Users should be able to recover/change lost passwords via having an e-mail sent to them.    
####Uploading & Deleting Images (Level 3)
In addition to their profile image users should also be allowed to add a background image. A user should be able to upload/change/delete both background & profile images. The lecture CGI examples include one for uploading a file.    
####Editing Information (Level 3)
A user should be able to edit their details and change their profile images.    
####Deleting Posts (Level 3)
A matelook user should also be able to delete any of their posts, comments or replies,
####Suspending/Deleting matelook Account (Level 3)
A matelook user not currently interested in matelook should be able to suspend their account. A suspended account is not visible to other users.    
A matelook user should also be able to delete their account completely.    
####Notifications (Level 3)
A user should be able to indicate they wish to be notified by e-mail in one of these events:
their zid is mentioned in a post, comment or reply
they get a mate request
####Including Links, Images & Videos (Level 3)
A user should be able to include links, images and videos in a post, comment or reply. These should be appropriately displayed when the item is viewed.    
####Privacy(Level 3)
A user should be able to make part or all of the content of their matelook page visible only to their mates.    
####Advanced Features (Level 4)
If you wish to obtain over 90% you should consider providing adding features beyond those above. marks will be available for extra features.    
