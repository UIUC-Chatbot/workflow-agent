class Issue():
    def __init__(self, title, body, labels, assignees, milestone, state, number, created_at, updated_at, closed_at, author, comments):
        self.title = title
        self.body = body
        self.labels = labels
        self.assignees = assignees
        self.milestone = milestone
        self.state = state
        self.number = number
        self.created_at = created_at
        self.updated_at = updated_at
        self.closed_at = closed_at
        self.author = author
        self.comments = comments
    
    def __str__(self):
        return f"Title: {self.title}\nBody: {self.body}\nLabels: {self.labels}\nAssignees: {self.assignees}\nMilestone: {self.milestone}\nState: {self.state}\nNumber: {self.number}\nCreated At: {self.created_at}\nUpdated At: {self.updated_at}\nClosed At: {self.closed_at}\nAuthor: {self.author}\nComments: {self.comments}"
    
    def format_issue(self):
        #   linked_pr = get_linked_pr_from_issue(issue)
        title = f"Title: {self.issue.title}."
        #   existing_pr = f"Existing PR addressing issue: {linked_pr}" if linked_pr else ""
        opened_by = f"Opened by user: {self.issue.opened_by}"
        body = f"Body: {self.issue.body}"
        return "\n".join([title, opened_by, body])