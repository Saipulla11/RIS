select segment, "year", "month", volume_night, volume_day
from report
where (%s::int is null or "year" = %s)
  and (%s::int is null or "month" = %s)
order by "year", "month", segment
