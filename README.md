# CNCF People
This repo stores the data that will populate the various people listings on cncf.io.  People can update their listing by submitting a PR to the repo.  The listings are:
- [Ambassadors](https://www.cncf.io/people/ambassadors/)
- [Governing Board](https://www.cncf.io/people/governing-board/)
- [Staff](https://www.cncf.io/people/staff/)
- [Technical Oversight Committee](https://www.cncf.io/people/technical-oversight-committee/)
- [TOC Contributors](https://www.cncf.io/people/technical-oversight-committee/#toc-contributors)

The [people.json file](https://github.com/cncf/people/blob/main/people.json) lists all people in alphabetical order by name.  Add new entries in the right place in the list.  This is the format:

```
    {
        "name":"Full name of person",
        "bio":"Full bio of person. Use html markup when necessary.",
        "company":"Company and/or title",
        "pronouns":"Personal pronouns",
        "location":"A Google Maps readable name of city, state, country",
        "linkedin":"LinkedIn url",
        "twitter":"Twitter url",
        "github":"GitHub url",
        "wechat":"Wechat url",
        "website":"Personal website",
        "youtube":"YouTube url",
        "priority":Value to diffentiate between other entries in an ordered list,
        "language":[Array of languages spoken],
        "projects":[Array of projects of expertise],
        "category":[Array of categories the person belongs to],
        "image":"Image filename from the /images/ directory"
    }
```

And here is an example entry:
```
    {
        "name":"Bartłomiej Płotka",
        "bio":"Bartek Plotka is a Principal Software Engineer at Red Hat with a background in SRE, currently working on Observability. As the co-author of the CNCF Thanos project and core maintainer of various open-source projects including Prometheus, he enjoys building OSS communities and maintainable, reliable distributed systems, ideally in Go. On top of that, he is active in the CNCF SIG Observability as the technical lead. He writes a book with O'Reilly.",
        "company":"Red Hat",
        "pronouns":"he/him",
        "location":"Portland, Oregon, USA",
        "linkedin":"https://www.linkedin.com/in/amy-wormley-7492954a/",
        "twitter":"https://twitter.com/bwplotka",
        "github":"https://github.com/cjyabraham",
        "wechat":"https://web.wechat.com/donaldliu1874",
        "website":"https://cjyabraham.com",
        "youtube":"https://www.youtube.com/c/cloudnativefdn",
        "priority":400,
        "language":["Hindi","English"],
        "projects":["prometheus","kubernetes","envoy"],
        "category":["Ambassadors","TOC Contributors"],
        "image":"bartlomeij-plotka.jpg"
    }
```
