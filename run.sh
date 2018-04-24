START=$(date +%s)
echo ============================================================================
echo "                        Run Vector Space Model                            "
echo ============================================================================
python3 VSM.py
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"
echo ============================================================================
echo "                Evaluation of ranked retrieval results                    "
echo ============================================================================
python3 Evaluation.py

