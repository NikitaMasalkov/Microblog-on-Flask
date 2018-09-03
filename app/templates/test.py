        add_minutes = int(form.minutesf.data)
        add_hours = int(form.hoursf.data)
        total_time.hours += add_hours
        total_time.minutes += add_minutes
        db.session.add(total_time)
        db.session.commit()