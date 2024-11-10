#!/bin/zsh

process_file() {
  local input_file="$1"
  local temp_output_file="${input_file%.*}_temp.mp4"
  local final_output_file="${input_file%.*}.mp4"
  
  # 元ファイルの変更日時
  local mod_time=$(stat -f "%m" "$input_file")

  # ffmpegでH.264/crf=18/mp4に
  ffmpeg -i "$input_file" -c:v libx264 -crf 18 "$temp_output_file"

  # 元の消して、日付戻して、名前変更
  if [ $? -eq 0 ]; then
    rm "$input_file"
    mv "$temp_output_file" "$final_output_file"
    touch -t $(date -r $mod_time +%Y%m%d%H%M.%S) "$final_output_file"
    echo "success: $final_output_file"
  else
    echo "failed: $input_file"
  fi
}

# フォルダorファイル
input_path="$1"

# if存在
if [ ! -e "$input_path" ]; then
  echo "pathが存在しません: $input_path"
  exit 1
fi

if [ -f "$input_path" ]; then
  # ファイル
  process_file "$input_path"
elif [ -d "$input_path" ]; then
  # フォルダ
  for file in "$input_path"/*; do
    if [[ "$file" == *.mp4 || "$file" == *.mov ]]; then
      process_file "$file"
    fi
  done
else
  echo "ファイルでもフォルダでもない..? : $input_path"
  exit 1
fi