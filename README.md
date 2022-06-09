# screaming_at_order_tracking_update

Yes. It's what it's. But this is for MacOS only (sorry, improvement point)


# Did you buy something at Submarino or Americanas and your order's carrier is [directlog](https://corporativo.directlog.com.br/) ? 

Can't you wait for your order and you keep into the website to see the current state of your tracking? Here's your hope.    


This is a script that keeps scraping the table from your order, and if we got some update, a voice will haunt you `"THERE WAS AN UPDATE ON YOUR PACK! check where your order is! it might be arriving!"` and promptly a csv containing the current table of your tracking will be exported to the same folder where the script is located. 

You just have to set a cronjob with this script, and in every execution, it will be checked if there's an update.   
*No updates = no voices = no csv.*

Ps: don't worry, a simple txt (last_number_of_lines.txt) will be created within the same folder, so we can check the old execution amount of lines against the current execution amount of lines. That's how we do this. If you delete this file, the execution will always consider we have an update.
 






