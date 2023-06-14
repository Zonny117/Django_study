class Quiz {
  String title;
  List<String> candidates;
  int answer;

  Quiz({
    required this.title,
    required this.answer,
    required this.candidates,
  });

  Quiz.fromMap(Map<String, dynamic> map)
      : title = map['title'],
        candidates = map['candidates'],
        answer = map['answer'];
}
