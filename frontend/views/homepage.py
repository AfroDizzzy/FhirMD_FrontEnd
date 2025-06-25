from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


SAMPLE_ITEMS = [
    {
        'id': 1, 
        'name': 'Task 1', 
        'description': 'Complete the project documentation',
        'details': 'This task involves writing comprehensive documentation for the entire project, including API documentation, user guides, and technical specifications.',
        'status': 'In Progress',
        'priority': 'High',
        'assigned_to': 'John Doe',
        'due_date': '2025-07-15'
    },
    {
        'id': 2, 
        'name': 'Task 2', 
        'description': 'Review code changes',
        'details': 'Conduct thorough code review for the latest pull requests, focusing on code quality, security, and performance improvements.',
        'status': 'Pending',
        'priority': 'Medium',
        'assigned_to': 'Jane Smith',
        'due_date': '2025-07-10'
    },
    {
        'id': 3, 
        'name': 'Task 3', 
        'description': 'Update database schema',
        'details': 'Modify the database schema to accommodate new features, including adding new tables and updating existing relationships.',
        'status': 'Not Started',
        'priority': 'High',
        'assigned_to': 'Mike Johnson',
        'due_date': '2025-07-20'
    },
    {
        'id': 4, 
        'name': 'Task 4', 
        'description': 'Deploy to production',
        'details': 'Deploy the latest version of the application to the production environment, including database migrations and server configuration updates.',
        'status': 'Ready',
        'priority': 'Critical',
        'assigned_to': 'Sarah Wilson',
        'due_date': '2025-07-25'
    },
    {
        'id': 5, 
        'name': 'Task 5', 
        'description': 'Run security tests',
        'details': 'Execute comprehensive security testing including penetration testing, vulnerability scanning, and security code review.',
        'status': 'In Progress',
        'priority': 'High',
        'assigned_to': 'Alex Brown',
        'due_date': '2025-07-18'
    },
]

def homepage(request):

    context = {
        'items': SAMPLE_ITEMS,
        'page_title': 'Django Home Page'
    }

    return render(request, 'frontend/homepage.html', context)