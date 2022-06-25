def text_sizer(nvars) :
  text_size = 12 - ((nvars + 1) / 8)
  if text_size > 12 :
    text_size = 12
  elif text_size < 1 :
    text_size = 0
  return text_size
