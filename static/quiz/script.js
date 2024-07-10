document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const data = new FormData(form);
        const result = {
            category_id: form.dataset.categoryId,
            score: 0,
            fail: 0,
            question_results: []
        };

        document.querySelectorAll('input[type="radio"]:checked').forEach((input) => {
            const questionId = input.name.split('_')[1];
            const selectedVariantId = input.value;
            const correctVariantId = input.dataset.correctVariantId;

            const isCorrect = selectedVariantId === correctVariantId;
            result.question_results.push({
                question_id: questionId,
                correct_variant_id: correctVariantId,
                selected_variant_id: selectedVariantId,
                is_correct: isCorrect
            });

            if (isCorrect) {
                result.score += 1;
            } else {
                result.fail += 1;
            }
        });

        document.cookie = `quiz_result=${JSON.stringify(result)}; path=/; max-age=3600`;

        form.submit();
    });
});
