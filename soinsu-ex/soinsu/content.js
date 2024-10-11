chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'showContent') {
        main_a();
        buttonClicked = true;
    } else if (msg.action === 'doNothing') {
        doNothing();
    }
});



function doNothing() {
    //何もしない
}


//よくわからん処理
//それっぽくしてみたかったけど無理だった、今後に期待
let buttonClicked = false;

window.onload = function () {
    if (buttonClicked) {
        main_a();
    }
};



async function main_a() {
    const elements = document.querySelectorAll('body *');
    var cc = 0;
    for (let element of elements) {
        if (element.children.length === 0 && element.textContent.trim() !== '' && !element.textContent.trim().startsWith("<") && !element.textContent.trim().includes("function") && !element.textContent.trim().includes("http")) {
            console.log("a");
            try {
                //デバック用
                cc += 1;
                if (cc >= 250) {
                    // window.alert(element.textContent.trim());
                }

                var normalized = element.textContent.trim().normalize("NFKC");
                normalized = normalized.replace(/\b0+(\d)/g, '$1');
                normalized = normalized.replace(/(\d),(\d{3})/g, '$1$2');
                var response = await replaceNumbersWithPrimeFactors(normalized);
                element.textContent = response;
            } catch (error) {
                console.log(error);
            }
        }
        console.log("c");
    }
    // window.alert("Done!")
}


async function primeFactors(n) {
    let same = [0, 1, 53];
    if (same.includes(n)) {
        return n;
    }

    const factors = [];
    let divisor = 2;

    while (n % divisor == 0) {
        factors.push(divisor);
        n = n / divisor;
    }

    divisor = 3;
    while (n >= 2 && divisor <= Math.sqrt(n)) {
        if (n % divisor == 0) {
            factors.push(divisor);
            n = n / divisor;
        } else {
            divisor += 2;
        }
    }

    if (n > 1) {
        factors.push(n);
    }

    return factors;
}



async function replaceNumbersWithPrimeFactors(text) {
    const regex = /\d+/g;
    let match;
    while ((match = regex.exec(text)) !== null) {
        const num = parseInt(match[0]);
        const factors = await primeFactors(num);
        const factorCounts = {};
        for (const factor of factors) {
            if (factorCounts[factor] === undefined) {
                factorCounts[factor] = 0;
            }
            factorCounts[factor]++;
        }
        let factorString = '';
        for (const factor in factorCounts) {
            if (factorCounts[factor] > 1) {
                factorString += factor + '^' + factorCounts[factor];
            } else {
                factorString += factor;
            }
            factorString += '×';
        }
        factorString = factorString.slice(0, -1);
        text = text.slice(0, match.index) + factorString + text.slice(match.index + match[0].length);
        regex.lastIndex = match.index + factorString.length;
    }
    return text;
}