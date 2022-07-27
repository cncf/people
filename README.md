# CNCF People
This repo stores the data that will populate the various people listings on cncf.io.  People can update their listing by submitting a PR for approval.  The listings are:
- [Ambassadors](https://www.cncf.io/people/ambassadors/)
- [Governing Board](https://www.cncf.io/people/governing-board/)
- [Staff](https://www.cncf.io/people/staff/)
- [Technical Oversight Committee](https://www.cncf.io/people/technical-oversight-committee/)

## Listing Format

The [people.json file](https://github.com/cncf/people/blob/main/people.json) lists all people in alphabetical order by name.  Add new entries in the right place in the list.  Not all fields are used by each listing.  This is the format:

```
    {
        "name":"Full name of person",
        "bio":"Full bio of person. Use html markup when needed.",
        "company":"Company and/or title",
        "pronouns":"Personal pronouns",
        "location":"A Google Maps readable name of city, state, country",
        "linkedin":"LinkedIn url",
        "twitter":"Twitter url",
        "github":"GitHub url",
        "wechat":"Wechat url",
        "website":"Personal website",
        "youtube":"YouTube url",
        "priority":Value to diffentiate between other entries in an ordered list; omit this entry in most cases,
        "languages":[Array of languages spoken],
        "projects":[Array of CNCF projects of expertise],
        "category":[Array of categories the person belongs to],
        "image":"Image filename from the /images/ directory"
    }
```
Project names must exactly match [the landscape listing](https://landscape.cncf.io/card-mode?project=hosted).  Category names must exactly match the list above.

And here is an example entry:
```
    {
        "name":"Johnny Appleseed",
        "bio":"John Chapman (September 26, 1774 – March 18, 1845), better known as Johnny Appleseed, was an American pioneer nurseryman who introduced apple trees to large parts of <a href='https://en.wikipedia.org/wiki/Pennsylvania'>Pennsylvania</a>, Ohio, Indiana, Illinois and Ontario, as well as the northern counties of present-day West Virginia. He became an American legend while still alive, due to his kind, generous ways, his leadership in conservation, and the symbolic importance he attributed to apples. He was also a missionary for The New Church (Swedenborgian)[1] and the inspiration for many museums and historical sites such as the Johnny Appleseed Museum[2] in Urbana, Ohio. The Fort Wayne TinCaps, a minor league baseball team in Fort Wayne, Indiana, where Chapman spent his final years, is named in his honor.",
        "company":"Apples R Us",
        "pronouns":"he/him",
        "location":"Portland, Maine, United States",
        "linkedin":"https://www.linkedin.com/in/johnny-appleseed/",
        "twitter":"https://twitter.com/jappleseed",
        "github":"https://github.com/jappleseed",
        "wechat":"https://web.wechat.com/jappleseed",
        "website":"https://jappleseed.com",
        "youtube":"https://www.youtube.com/c/jappleseed",
        "priority":10,
        "languages":["Spanish","English"],
        "projects":["prometheus","kubernetes","envoy"],
        "category":["Ambassadors","TOC Contributors"],
        "image":"jappleseed.jpg"
    }
```

## Images

Upload your headshot image to the `/images/` directory with a filename made up of your name.  Images should be at least 500x500px, 72dpi, and should be in JPG format with file size less than 100kB.
