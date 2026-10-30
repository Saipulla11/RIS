select old_balance, new_balance from balance_update where sub_id = %s and update_date::date = %s order by id
