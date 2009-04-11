# Map the Review domain model onto the review table
mapper(Review, review,
       properties = {
    'reviewer': relation(Person, lazy=True, backref='reviews'),
    'stream': relation(Stream, lazy=True),
    }
       )
