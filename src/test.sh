#!/bin/bash
# credits to AI CG :D

CHECKER_DIR=`dirname $0`/checker
TEST_SUITE=${1:-tests}
TEST_DIR=$CHECKER_DIR/${TEST_SUITE}
INPUT_FILE="dfa"
COND_ARGUMENTS="a u"
BIN_ARGUMENTS="e v f"

run_tests (){
        for arg in $1
        do
            test_files=$(find $TEST_DIR -type f | grep -E ".*-[a-z]*${arg}[a-z]*\.in$")

        current_score=0
        for input in $test_files
        do
            output=${input/.in/.${arg}}
            OUTPUT_FILE=$output.out
            ERROR_FILE=$output.err
            rm $INPUT_FILE $OUTPUT_FILE &> /dev/null
            cp ${input} $INPUT_FILE

            # Run the student homework
            timeout 3 make -s run arg=-$arg > $OUTPUT_FILE 2> $ERROR_FILE
            if [ $? -ne 0 ]
            then
                echo -e "\e[31mFAILED\e[0m Test (`basename $input`,$arg). You failed to win: $weight"
                echo "Timeout 3s"
            else

                cat $OUTPUT_FILE | sort > "$OUTPUT_FILE.sorted"

                total_score=$[total_score + $weight]

                diff -bBq "$OUTPUT_FILE.sorted" "${output}${test_extension}" &> /dev/null
                if [ $? -eq 0 ]
                then
                    echo -e "\e[32mPASSED\e[0m Test (`basename $input`,$arg). You won: $weight"
                    current_score=$[$current_score + $weight]; rm "${OUTPUT_FILE}"* "${ERROR_FILE}"
                else
                    echo -e "\e[31mFAILED\e[0m Test (`basename $input`,$arg). You failed to win: $weight"
                    echo " failed output -> $OUTPUT_FILE"
                    echo " sorted failed output -> $OUTPUT_FILE.sorted"
                    echo " official output -> ${output}${test_extension}"
                    echo " failed error output -> $ERROR_FILE"
                    if [[ $test_extension ]]
                    then
                        comm -12 "${OUTPUT_FILE}.sorted" "${output}.sorted" > "${output}.="
                        comm -13 "${OUTPUT_FILE}.sorted" "${output}.sorted" > "${output}.+"
                        comm -23 "${OUTPUT_FILE}.sorted" "${output}.sorted" > "${output}.-"
                        echo " missing, correct and surplus lines -> ${OUTPUT_FILE}.- ${OUTPUT_FILE}.= ${OUTPUT_FILE}.+"
                    fi
                fi
            fi

        done

        if [[ $current_score -gt 0 ]]
        then
            bonus_score=$[$bonus_score + 1]
        fi

        score=$[$score + $current_score]
    done
}


# Compile student homework
make build

# if missing, generate tests
echo "Generating tests"
python3 $CHECKER_DIR/testsetgen.py $TEST_SUITE

# Sort files for the first time
$CHECKER_DIR/sort.sh $TEST_SUITE >/dev/null

echo "Starting"

# Run tests
score=0
bonus_score=0
total_bonus_score=5
total_score=0
weight=1

test_extension='.sorted'

run_tests "$COND_ARGUMENTS"

echo "You have $score out of $total_score"

# comment the following line if you want to run all the tests
if [[ $score -lt $[$total_score / 2] ]]; then echo -e "\e[31mTests for -v and -f shall not run\e[0m ";total_bonus_score=3; BIN_ARGUMENTS="e"; fi

unset test_extension

run_tests "$BIN_ARGUMENTS"

score=$[$score + $bonus_score]
total_score=$[total_score + $total_bonus_score]

rm $INPUT_FILE &> /dev/null
make clean


echo "Score: $score out of $total_score"

make Flexer.java