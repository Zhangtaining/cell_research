import numpy as np
import statistics as st

bubble = [433, 673, 744, 681, 685, 651, 648, 656, 649, 622, 632, 664, 635, 591, 681, 710, 573, 580, 560, 634, 634, 607, 580, 674, 683, 649, 601, 626, 627, 520, 735, 528, 651, 619, 555, 669, 575, 542, 607, 610, 633, 469, 517, 663, 668, 597, 631, 623, 623, 526, 613, 637, 563, 747, 641, 627, 604, 637, 535, 697, 665, 615, 558, 548, 586, 653, 547, 598, 710, 566, 556, 636, 633, 657, 642, 551, 591, 582, 638, 604, 474, 659, 564, 517, 605, 552, 687, 664, 572, 599, 649, 594, 591, 620, 623, 661, 621, 607, 700, 533]

selection = [158, 134, 159, 180, 176, 154, 179, 201, 188, 155, 202, 140, 138, 193, 154, 184, 169, 155, 192, 166, 145, 146, 161, 129, 155, 165, 182, 157, 164, 191, 165, 161, 167, 188, 166, 161, 137, 162, 148, 150, 170, 151, 182, 180, 183, 168, 154, 172, 173, 191, 152, 171, 193, 162, 152, 178, 146, 181, 144, 199, 163, 187, 171, 151, 168, 164, 152, 161, 179, 176, 172, 172, 199, 153, 158, 177, 153, 160, 159, 177, 166, 154, 203, 182, 179, 151, 143, 139, 177, 143, 169, 148, 158, 127, 186, 136, 151, 144, 167, 149]

mixed_25pct_bubble = [412, 293, 267, 386, 289, 390, 341, 336, 299, 413, 310, 285, 410, 351, 262, 451, 383, 375, 415, 407, 352, 332, 355, 327, 385, 407, 237, 344, 298, 295, 393, 340, 295, 340, 297, 347, 388, 409, 353, 360, 345, 384, 355, 336, 304, 429, 452, 295, 291, 305, 307, 333, 410, 330, 276, 345, 341, 452, 243, 312, 266, 378, 241, 319, 383, 320, 251, 397, 375, 359, 291, 307, 324, 294, 410, 334, 258, 379, 389, 389, 317, 309, 372, 442, 267, 247, 428, 268, 320, 292, 373, 379, 290, 297, 353, 345, 451, 412, 313, 289]

mixed_50pct_bubble = [473, 475, 445, 546, 499, 546, 490, 508, 584, 579, 347, 496, 466, 462, 517, 479, 335, 481, 515, 562, 456, 461, 486, 397, 376, 476, 494, 492, 552, 427, 389, 485, 516, 530, 437, 444, 487, 393, 451, 527, 587, 422, 388, 609, 458, 496, 491, 410, 483, 435, 351, 502, 471, 437, 456, 480, 508, 473, 393, 479, 479, 390, 478, 464, 394, 415, 454, 494, 481, 501, 394, 409, 538, 440, 433, 509, 427, 534, 480, 495, 508, 459, 521, 497, 508, 454, 458, 395, 556, 653, 535, 377, 529, 417, 514, 428, 461, 446, 496, 487]

mixed_75pct_bubble = [510, 549, 547, 626, 571, 550, 654, 526, 586, 551, 535, 518, 562, 568, 526, 498, 578, 529, 578, 511, 564, 585, 560, 496, 472, 521, 550, 583, 553, 494, 484, 544, 622, 491, 541, 495, 476, 517, 503, 489, 537, 649, 607, 546, 512, 530, 454, 551, 567, 546, 574, 518, 503, 494, 581, 448, 494, 621, 594, 606, 554, 616, 602, 574, 573, 444, 602, 564, 564, 558, 528, 532, 656, 570, 518, 557, 472, 570, 530, 593, 638, 460, 611, 565, 582, 533, 551, 536, 585, 543, 548, 510, 498, 534, 403, 503, 410, 566, 495, 519]


print("Averge for each combination >>>>>>>>>>>>>>>>>")
print(f"Bubble (100%): {np.average(bubble)}")
print(f"Bubble (75%): {np.average(mixed_75pct_bubble)}")
print(f"Bubble (50%): {np.average(mixed_50pct_bubble)}")
print(f"Bubble (25%): {np.average(mixed_25pct_bubble)}")
print(f"Bubble (0%): {np.average(selection)}")



print("Median for each combination >>>>>>>>>>>>>>>>>")
print(f"Bubble (100%): {st.median(bubble)}")
print(f"Bubble (75%): {st.median(mixed_75pct_bubble)}")
print(f"Bubble (50%): {st.median(mixed_50pct_bubble)}")
print(f"Bubble (25%): {st.median(mixed_25pct_bubble)}")
print(f"Bubble (0%): {st.median(selection)}")



print("Stdev for each combination >>>>>>>>>>>>>>>>>")
print(f"Bubble (100%): {np.std(bubble)}")
print(f"Bubble (75%): {np.std(mixed_75pct_bubble)}")
print(f"Bubble (50%): {np.std(mixed_50pct_bubble)}")
print(f"Bubble (25%): {np.std(mixed_25pct_bubble)}")
print(f"Bubble (0%): {np.std(selection)}")


print("Max for each combination >>>>>>>>>>>>>>>>>")
print(f"Bubble (100%): {max(bubble)}")
print(f"Bubble (75%): {max(mixed_75pct_bubble)}")
print(f"Bubble (50%): {max(mixed_50pct_bubble)}")
print(f"Bubble (25%): {max(mixed_25pct_bubble)}")
print(f"Bubble (0%): {max(selection)}")



