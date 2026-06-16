def should_store(message: str) -> bool:

    text = message.lower().strip()

    if not text:
        return False

    # Pure URLs
    if text.startswith("http") and len(text.split()) < 5:
        return False

    # Women-only
    women_only_keywords = [
        "women engineers",
        "women-in-tech",
        "women only",
        "female candidates",
        "girls only",
        "women students",
        "weforshe"
    ]

    # Updates (process/logistics, not opportunities)
    update_keywords = [
        "online test updates",
        "online test schedule",           # NEW: catches "Zopsmart Online Test Schedule"
        "test schedule",                  # NEW
        "venue update",                   # NEW: catches "Venue Updates"
        "reporting time",                 # NEW: catches test venue messages
        "oa link",
        "interview schedule",
        "gd link",
        "group discussion",
        "assessment report",
        "candidate monitoring",
        "shortlisted",
        "results announced",
    ]

    # Definitely ignore
    ignore_keywords = [
        "webinar",
        "career guidance",
        "learning program",
        "certification",
        "virtual session",
        "microsoft ai skill fest",
        "salesforce",
        "bobathon",
        "bootcamp",
        "workshop",
        "important message to all students",
        "malpractice",
        "blacklisted",
        "disciplinary",
        "NeoPAT",
        "placement preparation",
        "placement-ready",
        "day report",
        "neopat",
        "student portal",
        "activated status",
        # REMOVED "assessment" — too broad, kills real JDs with "Assessment" interview rounds
        "freshers hiring trend",
        "scholarship",
        "mext",
        "iet india scholarship",
        "counselling",
        "seat allocation",
        "students who have applied",
        "important notice",
        "please avoid applying",
        "only relevant profiles will be considered",
        "aptitude challenge",
        "ncat",
        "aptitude test",
        "60 days assessment",             # NEW: specific NeoPAT-style messages
        "not yet completed the registration",  # NEW: catches Zenken/registration nudges
        "freshers platform",              # NEW: catches "Zenken Yaaay Freshers Platform"
        "complete the registration",      # NEW
        "kindly check your mail",         # NEW: admin nudge messages
        "neo score",                      # NEW: NeoPAT scoring system
        "level 1 to level 4",            # NEW: NeoPAT levels
        "upskilling",                     # NEW: generic skill-push, not a job post
    ]

    for word in women_only_keywords:
        if word in text:
            return False

    for word in update_keywords:
        if word in text:
            return False

    for word in ignore_keywords:
        if word in text:
            return False

    # Hackathon handling — only keep if there's a concrete hiring outcome
    if "hackathon" in text or "hackerramp" in text:

        hiring_hackathon_keywords = [
            "guaranteed internship",
            "guaranteed interview",
            "guaranteed ppo",
            "guaranteed ppi",
            "direct hiring",
            "full time offer",
            "fte",
            "internship opportunity",
            "stipend",                    # NEW: some hackathons mention stipend for winners
            "pre-placement",              # NEW
            "ppo",                        # NEW
        ]

        return any(
            keyword in text
            for keyword in hiring_hackathon_keywords
        )

    challenge_keywords = [
        "coding challenge",
        "tech challenge",
        "competition",
        "academic challenge",
    ]

    if any(word in text for word in challenge_keywords):

        hiring_signals = [
            "direct hiring",
            "internship role",
            "full-time role",
            "fte",
            "job role",
            "stipend",
            "salary"
        ]

        return any(
            signal in text
            for signal in hiring_signals
        )

    # Actual job signals
    job_signals = [
        "placement opportunity",
        "internship opportunity",
        "internship",
        "hiring",
        "recruitment",
        "stipend",
        "ctc",
        "package",
        "full-time",
        "full time",
        "fte",
        "eligible branches",
        "bond",
        "service agreement",
        "job description",
    ]

    return any(
        signal in text
        for signal in job_signals
    )