from django.shortcuts import render


def get_grade(marks):
    if marks >= 80:
        return "A+"
    elif marks >= 70:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


def index(request):
    result = None
    error = None

    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()

            if not name:
                raise ValueError("Please enter student name.")

            subjects = {
                "English": int(request.POST.get("english")),
                "Mathematics": int(request.POST.get("math")),
                "Computer": int(request.POST.get("computer")),
                "Physics": int(request.POST.get("physics")),
                "Pakistan Studies": int(request.POST.get("pakistan")),
            }

            # Check marks
            if any(mark < 0 or mark > 100 for mark in subjects.values()):
                raise ValueError("Marks must be between 0 and 100.")

            # Calculate total and percentage
            total = sum(subjects.values())
            percentage = total / 5

            # Subject-wise results
            subject_results = []

            for subject, marks in subjects.items():
                subject_results.append({
                    "name": subject,
                    "marks": marks,
                    "grade": get_grade(marks),
                })

            # Final grade
            final_grade = get_grade(percentage)

            # Student must have at least 40 marks in every subject
            status = "Pass" if percentage >= 40 and all(
                mark >= 40 for mark in subjects.values()
            ) else "Fail"

            result = {
                "name": name,
                "subjects": subject_results,
                "total": total,
                "percentage": percentage,
                "grade": final_grade,
                "status": status,
            }

        except (ValueError, TypeError):
            error = "Please enter valid marks between 0 and 100."

    return render(
        request,
        "grades/index.html",
        {
            "result": result,
            "error": error,
        }
    )