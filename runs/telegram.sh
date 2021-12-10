#!/bin/bash
curl -X POST 'https://api.telegram.org/bot'"$telegramtoken"'/sendMessage?chat_id='"$telegramuser"'&text='"${1}"''
