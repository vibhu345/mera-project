import sys
# Tum sys module ka use kar rahe ho taaki tum exception ke detailed information ko store kar sako, jaise ki line number, file name, etc., jise tum custom exception ke saath associate kar sakte ho.
class CustomException(Exception):
    
    def __init__(self,error_message,error_detail:sys):
#         error_message: Tumhare custom exception ka error message, jo tum exception raise karte waqt pass karte ho.
# error_details: Yeh parameter sys module se related hai, jo exception ke details ko capture karne ke liye use hoga (Jaise ki error ka type, line number, etc.).
        super().__init__(error_message)
        _, _, exc_tb=error_detail.exc_info()
        # error_detail.exc_info() → यह function तीन चीजें return करता है:
        # exc_type → Error का type (e.g., ValueError, TypeError etc.)
        # exc_obj → Exception का object
        # exc_tb → Traceback object, जो error के बारे में details रखता है (जैसे line number, file name)
        file_name=exc_tb.tb_frame.f_code.co_filename
        # exc_tb.tb_frame.f_code.co_filename
         #tb_frame → जिस function में error हुआ, उसका frame देता है।
        # f_code → उस function के code object को देता है।
        # co_filename → जिस Python script में error हुआ, उसका नाम देता है
        self.error_message="Error occured python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error_message))



    def __str__(self):
        # __str__ method object को string में बदलने के लिए होता है, ताकि print(object) करने पर custom readable message दिखे, न कि default object representation।
        return self.error_message
