{{ dbt_utils.date_spine(
  datepart="month",
  start_date="cast('2011-02-01' as date)",
  end_date="cast('2024-01-01' as date)"
) }}