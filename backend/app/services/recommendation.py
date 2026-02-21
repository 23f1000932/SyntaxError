from app.models.event import Event
from app.models.registration import Registration
from app.extensions import db
from sqlalchemy import func, case
from datetime import datetime, timedelta


class RecommendationService:
    """
    Priority stack (Features 1-4):
      1. Preferred sports match   (+4)
      2. City match               (+3)
      3. Budget tier match        (+2)
      4. Within next 7 days       (+1)
      5. Fallback: popular (registration count)
    """

    @staticmethod
    def get_recommended(user, limit=20):
        q = Event.query.filter(Event.is_active == True)

        if user:
            sports = user.preferred_sports or []
            city = user.city
            budget = user.budget_preference

            sport_score = case(
                (Event.sport_category.in_(sports), 4), else_=0
            ) if sports else 0

            city_score = case(
                (Event.venue_city == city, 3), else_=0
            ) if city else 0

            budget_score = case(
                (Event.price_tier == budget, 2), else_=0
            ) if budget else 0

            week_end = datetime.utcnow() + timedelta(days=7)
            date_score = case(
                (Event.event_date <= week_end, 1), else_=0
            )

            total = date_score
            if sports:
                total = total + sport_score
            if city:
                total = total + city_score
            if budget:
                total = total + budget_score

            q = q.order_by(total.desc(), Event.event_date.asc())
        else:
            # Anonymous users: sort by popularity
            reg_count = db.session.query(
                Registration.event_id,
                func.count(Registration.id).label('cnt')
            ).group_by(Registration.event_id).subquery()

            q = q.outerjoin(
                reg_count, Event.id == reg_count.c.event_id
            ).order_by(
                func.coalesce(reg_count.c.cnt, 0).desc()
            )

        return q.limit(limit).all()

    @staticmethod
    def get_similar(event, limit=5):
        """Feature 5 – Same sport + city, ranked by registrations."""
        reg_count = db.session.query(
            Registration.event_id,
            func.count(Registration.id).label('cnt')
        ).group_by(Registration.event_id).subquery()

        return Event.query.filter(
            Event.id != event.id,
            Event.is_active == True,
            Event.sport_category == event.sport_category,
            Event.venue_city == event.venue_city
        ).outerjoin(
            reg_count, Event.id == reg_count.c.event_id
        ).order_by(
            func.coalesce(reg_count.c.cnt, 0).desc()
        ).limit(limit).all()
